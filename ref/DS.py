#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Vte', '2.91')
from gi.repository import Gtk, Gdk, GLib, Pango, Vte
import os
import asyncio
import json
import re

class SettingsDialog(Gtk.Dialog):
    def __init__(self, parent, current_settings):
        super().__init__(title="Settings", transient_for=parent, flags=0)
        self.set_default_size(400, 250)
        
        # Add buttons
        self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)
        self.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        
        box = self.get_content_area()
        box.set_spacing(10)
        box.set_margin_start(10)
        box.set_margin_end(10)
        box.set_margin_top(10)
        box.set_margin_bottom(10)
        
        # Provider selection
        provider_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        provider_label = Gtk.Label(label="Provider:")
        self.provider_combo = Gtk.ComboBoxText()
        providers = ["gemini", "openai", "anthropic"]
        for provider in providers:
            self.provider_combo.append_text(provider)
        if current_settings.get('provider'):
            self.provider_combo.set_active_id(current_settings['provider'])
        else:
            self.provider_combo.set_active(0)
        provider_box.pack_start(provider_label, False, False, 0)
        provider_box.pack_start(self.provider_combo, True, True, 0)
        
        # API Key entry
        api_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        api_label = Gtk.Label(label="API Key:")
        self.api_entry = Gtk.Entry()
        self.api_entry.set_visibility(False)
        if current_settings.get('api_key'):
            self.api_entry.set_text(current_settings['api_key'])
        api_box.pack_start(api_label, False, False, 0)
        api_box.pack_start(self.api_entry, True, True, 0)
        
        # Model selection
        model_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        model_label = Gtk.Label(label="Model:")
        self.model_entry = Gtk.Entry()
        if current_settings.get('model'):
            self.model_entry.set_text(current_settings['model'])
        else:
            self.model_entry.set_text("gemini-pro")
        model_box.pack_start(model_label, False, False, 0)
        model_box.pack_start(self.model_entry, True, True, 0)
        
        box.add(provider_box)
        box.add(api_box)
        box.add(model_box)
        self.show_all()

class DeepShellWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Deep Shell")
        
        self.chat_history = []
        self.settings = self.load_settings()
        if not self.settings:
            self.settings = {
                'provider': 'gemini',
                'model': 'gemini-pro',
                'api_key': ''
            }
        
        # Window setup
        self.set_default_size(1000, 700)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        # Enable transparency
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual and screen.is_composited():
            self.set_visual(visual)
            self.set_app_paintable(True)
        
        # Apply CSS
        self.setup_css()
        
        # Create main layout - single panel for chat interface
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.main_box)
        
        # Header with title and shell icon
        self.create_header()
        
        # Control panel
        self.create_control_panel()
        
        # Chat area
        self.create_chat_area()
        
        # Input area
        self.create_input_area()
        
        # Apply styles
        self.get_style_context().add_class("deep-shell-window")
        
    def setup_css(self):
        css_provider = Gtk.CssProvider()
        css_data = """
        .deep-shell-window {
            background-color: rgba(26, 27, 30, 0.95);
            color: white;
        }
        
        .header-box {
            background-color: rgba(30, 30, 30, 0.95);
            padding: 12px 16px;
            border-bottom: 1px solid rgba(44, 46, 51, 0.95);
        }
        
        .title-label {
            color: white;
            font-size: 18px;
            font-weight: bold;
        }
        
        .control-panel {
            background-color: rgba(30, 30, 30, 0.95);
            padding: 8px 16px;
            border-bottom: 1px solid rgba(44, 46, 51, 0.95);
        }
        
        .control-button {
            background-color: rgba(51, 51, 51, 0.95);
            color: white;
            border: none;
            border-radius: 6px;
            padding: 6px 12px;
            margin: 0 4px;
        }
        
        .control-button:hover {
            background-color: rgba(76, 78, 83, 0.95);
        }
        
        .messages-scroll {
            background-color: rgba(26, 27, 30, 0.95);
        }
        
        .message-user {
            background-color: rgba(49, 49, 49, 0.95);
            color: white;
            border-radius: 12px;
            padding: 12px 16px;
            margin: 8px 16px 8px 64px;
        }
        
        .message-assistant {
            background-color: rgba(35, 35, 35, 0.95);
            color: white;
            border-radius: 12px;
            padding: 12px 16px;
            margin: 8px 64px 8px 16px;
        }
        
        .input-container {
            background-color: rgba(26, 27, 30, 0.95);
            padding: 16px;
            border-top: 1px solid rgba(44, 46, 51, 0.95);
        }
        
        .message-input {
            background-color: rgba(51, 51, 51, 0.95);
            color: white;
            border: 1px solid rgba(76, 78, 83, 0.95);
            border-radius: 20px;
            padding: 12px 16px;
        }
        
        .message-input:focus {
            background-color: rgba(64, 64, 64, 0.95);
            border-color: rgba(100, 100, 100, 0.95);
        }
        
        .send-button {
            background-color: rgba(43, 87, 151, 0.95);
            color: white;
            border: none;
            border-radius: 50%;
            padding: 8px;
            margin-left: 8px;
        }
        
        .send-button:hover {
            background-color: rgba(60, 100, 170, 0.95);
        }
        
        .command-block {
            background-color: rgba(0, 0, 0, 0.4);
            border-left: 3px solid rgba(43, 87, 151, 0.95);
            border-radius: 4px;
            padding: 8px 12px;
            margin: 4px 0;
            font-family: monospace;
        }
        
        .run-button {
            background-color: rgba(43, 87, 151, 0.95);
            color: white;
            border: none;
            border-radius: 50%;
            padding: 4px;
            min-width: 24px;
            min-height: 24px;
        }
        
        .run-button:hover {
            background-color: rgba(60, 100, 170, 0.95);
        }
        """
        
        css_provider.load_from_data(css_data.encode())
        Gtk.StyleContext.add_provider_for_screen(
            self.get_screen(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
    
    def create_header(self):
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        header_box.get_style_context().add_class("header-box")
        
        # Shell icon
        shell_icon = Gtk.Image.new_from_icon_name("utilities-terminal", Gtk.IconSize.LARGE_TOOLBAR)
        header_box.pack_start(shell_icon, False, False, 0)
        
        # Title
        title_label = Gtk.Label(label="Deep Shell")
        title_label.get_style_context().add_class("title-label")
        header_box.pack_start(title_label, False, False, 0)
        
        # Settings button (right aligned)
        settings_button = Gtk.Button()
        settings_icon = Gtk.Image.new_from_icon_name("preferences-system", Gtk.IconSize.BUTTON)
        settings_button.add(settings_icon)
        settings_button.get_style_context().add_class("control-button")
        settings_button.connect("clicked", self.on_settings_clicked)
        header_box.pack_end(settings_button, False, False, 0)
        
        self.main_box.pack_start(header_box, False, False, 0)
    
    def create_control_panel(self):
        control_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        control_box.get_style_context().add_class("control-panel")
        
        # Auto Run toggle
        auto_run_label = Gtk.Label(label="Auto Run")
        auto_run_label.set_markup("<span color='white'>Auto Run</span>")
        self.auto_run_switch = Gtk.CheckButton()
        
        control_box.pack_start(auto_run_label, False, False, 0)
        control_box.pack_start(self.auto_run_switch, False, False, 0)
        
        # Reset button
        reset_button = Gtk.Button(label="Reset")
        reset_button.get_style_context().add_class("control-button")
        control_box.pack_end(reset_button, False, False, 0)
        
        self.main_box.pack_start(control_box, False, False, 0)
    
    def create_chat_area(self):
        # Scrolled window for messages
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.get_style_context().add_class("messages-scroll")
        
        # Messages container
        self.messages_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        scrolled.add(self.messages_box)
        
        self.main_box.pack_start(scrolled, True, True, 0)
        
        # Add initial greeting
        self.add_assistant_message("Hello! How can I assist you with the terminal today?")
    
    def create_input_area(self):
        input_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        input_container.get_style_context().add_class("input-container")
        
        # Text entry
        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Type your message...")
        self.entry.get_style_context().add_class("message-input")
        self.entry.connect("activate", self.on_entry_activate)
        
        # Send button
        send_button = Gtk.Button()
        send_icon = Gtk.Image.new_from_icon_name("go-next", Gtk.IconSize.BUTTON)
        send_button.add(send_icon)
        send_button.get_style_context().add_class("send-button")
        send_button.connect("clicked", self.on_entry_activate)
        
        input_container.pack_start(self.entry, True, True, 0)
        input_container.pack_start(send_button, False, False, 0)
        
        self.main_box.pack_start(input_container, False, False, 0)
    
    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
    
    def save_settings(self):
        with open('settings.json', 'w') as f:
            json.dump(self.settings, f)
    
    def on_settings_clicked(self, button):
        dialog = SettingsDialog(self, self.settings)
        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            self.settings['provider'] = dialog.provider_combo.get_active_text()
            self.settings['api_key'] = dialog.api_entry.get_text()
            self.settings['model'] = dialog.model_entry.get_text()
            self.save_settings()
        
        dialog.destroy()
    
    def add_message(self, text, message_type):
        message_label = Gtk.Label()
        message_label.set_markup(text)
        message_label.set_line_wrap(True)
        message_label.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)
        message_label.set_xalign(0)
        
        if message_type == "user":
            message_label.get_style_context().add_class("message-user")
        else:
            message_label.get_style_context().add_class("message-assistant")
        
        self.messages_box.pack_start(message_label, False, False, 0)
        message_label.show()
        
        # Auto scroll to bottom
        def scroll_to_bottom():
            adj = self.messages_box.get_parent().get_vadjustment()
            adj.set_value(adj.get_upper() - adj.get_page_size())
        GLib.idle_add(scroll_to_bottom)
    
    def add_user_message(self, text):
        self.add_message(text, "user")
    
    def add_assistant_message(self, text):
        self.add_message(text, "assistant")
    
    async def get_ai_response(self, text):
        # Simulate AI response - replace with actual AI integration
        await asyncio.sleep(1)
        if "conda" in text.lower():
            return "I can help you create a conda environment! Here's how:\n\n```bash\nconda create -n myenv python=3.9\nconda activate myenv\n```\n\nThis creates a new environment called 'myenv' with Python 3.9."
        else:
            return f"I understand you're asking about: {text}\n\nI can help with terminal commands, file operations, and system administration tasks."
    
    def on_entry_activate(self, widget):
        text = self.entry.get_text().strip()
        if not text:
            return
        
        self.add_user_message(text)
        self.entry.set_text("")
        
        async def get_response():
            try:
                response = await self.get_ai_response(text)
                GLib.idle_add(self.add_assistant_message, response)
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                GLib.idle_add(self.add_assistant_message, error_msg)
        
        asyncio.run(get_response())

def main():
    win = DeepShellWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    
    if not win.settings.get('api_key'):
        win.on_settings_clicked(None)
    
    Gtk.main()

if __name__ == "__main__":
    main()
