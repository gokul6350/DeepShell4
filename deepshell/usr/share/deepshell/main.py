#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Vte', '2.91')
from gi.repository import Gtk, Gdk, GLib, Pango, Vte
import os
import asyncio
from LLMHandler import deepshellai, LLMHandler
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
        for provider in LLMHandler.SUPPORTED_PROVIDERS.keys():
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
        self.api_entry.set_visibility(False)  # Hide API key
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
            self.model_entry.set_text(LLMHandler.SUPPORTED_PROVIDERS['gemini']['default_model'])
        model_box.pack_start(model_label, False, False, 0)
        model_box.pack_start(self.model_entry, True, True, 0)
        
        # Add all boxes to dialog
        box.add(provider_box)
        box.add(api_box)
        box.add(model_box)
        self.show_all()

class DeepShellWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="DeepShell AI - Your Terminal Copilot")
        self.set_wmclass("DeepShell4", "DeepShell4")
        # Initialize chat history
        self.chat_history = []
        
        # Load settings
        self.settings = self.load_settings()
        if not self.settings:
            self.settings = {
                'provider': 'gemini',
                'model': LLMHandler.SUPPORTED_PROVIDERS['gemini']['default_model'],
                'api_key': ''
            }
        
        # Set up window properties
        self.set_default_size(1200, 700)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        # Enable transparency
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual and screen.is_composited():
            self.set_visual(visual)
            self.set_app_paintable(True)
        
        # Set up CSS provider
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
        
        .message {
            margin: 8px 16px;
            padding: 12px 16px;
            border-radius: 12px;
            color: white;
        }
        
        .message.user {
            background-color: rgba(49, 49, 49, 0.95);
            margin-left: 64px;
        }
        
        .message.assistant {
            background-color: rgba(35, 35, 35, 0.95);
            margin-right: 64px;
        }
        
        .input-container {
            background-color: rgba(26, 27, 30, 0.95);
            border-top: 1px solid rgba(44, 46, 51, 0.95);
        }
        
        .message-input {
            background-color: rgba(51, 51, 51, 0.95);
            color: white;
            border: 1px solid rgba(76, 78, 83, 0.95);
            border-radius: 20px;
            padding: 8px 12px;
            margin: 8px;
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
            padding: 4px;
            min-width: 28px;
            min-height: 28px;
            margin: 8px;
        }
        
        .send-button:hover {
            background-color: rgba(60, 100, 170, 0.95);
        }
        
        .send-button image {
            padding: 0;
            margin: 0;
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
        
        .terminal-panel {
            background-color: rgba(30, 30, 30, 0.95);
        }
        
        .chat-panel {
            background-color: rgba(30, 30, 30, 0.95);
        }
        """
        css_provider.load_from_data(css_data.encode())
        Gtk.StyleContext.add_provider_for_screen(
            screen,
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        
        # Main paned container for resizable panels
        self.main_paned = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        self.add(self.main_paned)
        
        # Left panel for chat interface
        self.chat_panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.chat_panel.get_style_context().add_class("chat-panel")
        self.main_paned.add1(self.chat_panel)
        
        # Header bar with title, controls, and settings
        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        header.get_style_context().add_class("header-box")
        
        # Left side: Logo and title
        left_header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        logo_image = Gtk.Image.new_from_icon_name("utilities-terminal", Gtk.IconSize.LARGE_TOOLBAR)
        title_label = Gtk.Label(label="DeepShell AI")
        title_label.get_style_context().add_class("title-label")
        
        left_header.pack_start(logo_image, False, False, 0)
        left_header.pack_start(title_label, False, False, 0)
        
        # Center: Auto Run control
        center_header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        auto_run_label = Gtk.Label(label="Auto Run")
        auto_run_label.set_markup("<span color='white'>Auto Run</span>")
        self.auto_run_switch = Gtk.CheckButton()
        
        center_header.pack_start(auto_run_label, False, False, 0)
        center_header.pack_start(self.auto_run_switch, False, False, 0)
        
        # Right side: Settings and Reset buttons
        right_header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        
        # Reset button
        reset_button = Gtk.Button()
        reset_icon = Gtk.Image.new_from_icon_name("view-refresh", Gtk.IconSize.BUTTON)
        reset_button.add(reset_icon)
        reset_button.set_tooltip_text("Reset Terminal")
        reset_button.get_style_context().add_class("control-button")
        
        # Settings button
        settings_button = Gtk.Button()
        settings_icon = Gtk.Image.new_from_icon_name("preferences-system", Gtk.IconSize.BUTTON)
        settings_button.add(settings_icon)
        settings_button.get_style_context().add_class("control-button")
        settings_button.connect("clicked", self.on_settings_clicked)
        
        right_header.pack_end(settings_button, False, False, 0)
        right_header.pack_end(reset_button, False, False, 0)
        
        # Pack all sections into header
        header.pack_start(left_header, False, False, 0)
        header.set_center_widget(center_header)
        header.pack_end(right_header, False, False, 0)
        
        self.chat_panel.pack_start(header, False, False, 0)
        
        # Messages ScrolledWindow
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.get_style_context().add_class("messages-scroll")
        self.chat_panel.pack_start(scrolled, True, True, 0)
        
        # Messages container
        self.messages_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.messages_box.set_margin_start(16)
        self.messages_box.set_margin_end(16)
        self.messages_box.set_margin_top(16)
        self.messages_box.set_margin_bottom(16)
        scrolled.add(self.messages_box)
        
        # Add initial greeting message
        self.add_assistant_message("👋 Hello! How can I assist you with the terminal today?")
        
        # Input area
        input_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        input_box.set_margin_start(8)
        input_box.set_margin_end(8)
        input_box.set_margin_top(0)
        input_box.set_margin_bottom(0)
        input_box.get_style_context().add_class("input-container")
        
        # Text input
        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Ask me anything about the terminal...")
        self.entry.connect("activate", self.on_entry_activate)
        self.entry.get_style_context().add_class("message-input")
        input_box.pack_start(self.entry, True, True, 0)
        
        # Send button
        send_button = Gtk.Button()
        send_icon = Gtk.Image.new_from_icon_name("go-next", Gtk.IconSize.SMALL_TOOLBAR)
        send_button.add(send_icon)
        send_button.connect("clicked", self.on_entry_activate)
        send_button.get_style_context().add_class("send-button")
        input_box.pack_end(send_button, False, False, 0)
        
        self.chat_panel.pack_end(input_box, False, False, 0)
        
        # Right panel for terminal
        self.terminal_panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.terminal_panel.get_style_context().add_class("terminal-panel")
        self.main_paned.add2(self.terminal_panel)
        
        # Create terminal
        self.terminal = Vte.Terminal()
        self.terminal.set_cursor_blink_mode(Vte.CursorBlinkMode.ON)
        self.terminal.set_cursor_shape(Vte.CursorShape.IBEAM)
        
        # Set terminal colors
        background_color = Gdk.RGBA()
        background_color.parse('rgba(30,30,30,0.95)')
        foreground_color = Gdk.RGBA()
        foreground_color.parse('rgba(230,230,230,1.0)')
        
        self.terminal.set_color_background(background_color)
        self.terminal.set_color_foreground(foreground_color)
        
        # Set terminal font
        self.terminal.set_font(Pango.FontDescription("MonoSpace 10"))
        
        # Start shell in terminal
        self.terminal.spawn_sync(
            Vte.PtyFlags.DEFAULT,
            os.environ['HOME'],
            ["/bin/bash"],
            [],
            GLib.SpawnFlags.DO_NOT_REAP_CHILD,
            None,
            None,
        )
        
        # Add terminal to panel
        self.terminal_panel.pack_start(self.terminal, True, True, 0)
        
        # Set initial position of the pane divider
        self.main_paned.set_position(600)
        
    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                # Set environment variable
                if settings.get('api_key'):
                    provider = settings.get('provider', 'gemini')
                    env_key = LLMHandler.SUPPORTED_PROVIDERS[provider]['env_key']
                    os.environ[env_key] = settings['api_key']
                return settings
        except FileNotFoundError:
            return None
    
    def save_settings(self):
        with open('settings.json', 'w') as f:
            json.dump(self.settings, f)
    
    def on_settings_clicked(self, button):
        dialog = SettingsDialog(self, self.settings)
        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            # Update settings
            self.settings['provider'] = dialog.provider_combo.get_active_text()
            self.settings['api_key'] = dialog.api_entry.get_text()
            self.settings['model'] = dialog.model_entry.get_text()
            
            # Update environment variable
            env_key = LLMHandler.SUPPORTED_PROVIDERS[self.settings['provider']]['env_key']
            os.environ[env_key] = self.settings['api_key']
            
            # Save settings
            self.save_settings()
        
        dialog.destroy()
    
    async def get_ai_response(self, text):
        try:
            response, self.chat_history = await deepshellai(
                provider=self.settings['provider'],
                model_name=self.settings['model'],
                chat_history=self.chat_history,
                question=text
            )
            return response
        except Exception as e:
            return f"Error: {str(e)}"
    
    def extract_commands(self, text):
        """Extract commands from text that are wrapped in ```run blocks"""
        pattern = r"```run\n(.*?)```"
        commands = re.findall(pattern, text, re.DOTALL)
        return [cmd.strip() for cmd in commands]

    def execute_command(self, command):
        """Execute a command in the terminal"""
        command_bytes = (command + "\n").encode('utf-8')
        self.terminal.feed_child(command_bytes)

    def create_run_button(self, command):
        """Create a run button for a command"""
        button = Gtk.Button()
        button.set_tooltip_text("Run command")
        icon = Gtk.Image.new_from_icon_name("media-playback-start", Gtk.IconSize.SMALL_TOOLBAR)
        button.add(icon)
        button.get_style_context().add_class("run-button")
        button.connect("clicked", lambda btn: self.execute_command(command))
        return button

    def format_message_for_display(self, text_with_commands):
        """
        Processes text containing ```run...``` blocks for display.
        Returns:
            - processed_text: Text with ```run...``` blocks replaced by placeholders.
            - command_details: A list of dicts, each with {"placeholder": str, "command_str": str}.
        """
        command_details = []
        
        def replacer_func(match_obj):
            command_str = match_obj.group(1).strip()
            placeholder_index = len(command_details) 
            placeholder = f"__CMD_PLACEHOLDER_{placeholder_index}__"
            
            command_details.append({
                "placeholder": placeholder,
                "command_str": command_str
            })
            return placeholder

        pattern = r"```run\n(.*?)```"
        
        processed_text = re.sub(pattern, replacer_func, text_with_commands, flags=re.DOTALL)
        
        return processed_text, command_details

    def add_message(self, text_content, message_type):
        # Create a container for alignment
        align = Gtk.Alignment()
        if message_type == "user":
            align.set(1.0, 0, 0.85, 1)  # Right align, use 85% width
        else:
            align.set(0, 0, 0.85, 1)  # Left align, use 85% width
        
        # Message box
        message_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        message_box.get_style_context().add_class("message")
        message_box.get_style_context().add_class(message_type)
        
        if message_type == "assistant":
            # text_content is the original LLM response.
            # Auto-run has been handled by the caller (on_entry_activate).
            
            processed_text_for_display, command_details = self.format_message_for_display(text_content)
            
            # This container will hold all parts of the message (text labels, command blocks)
            message_content_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
            message_content_container.set_margin_start(12)
            message_content_container.set_margin_end(12)
            message_content_container.set_margin_top(8)
            message_content_container.set_margin_bottom(8)

            if not command_details:
                # No commands, just display the text as is (it might have Pango markup from LLM)
                label = Gtk.Label()
                label.set_markup(processed_text_for_display) # processed_text_for_display is original text
                label.set_line_wrap(True)
                label.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)
                label.set_xalign(0)
                message_content_container.pack_start(label, False, False, 0)
            else:
                # There are commands, so split the text by placeholders
                placeholders_pattern = "|".join([re.escape(cd["placeholder"]) for cd in command_details])
                # The pattern includes capturing parentheses to keep delimiters
                text_parts = re.split(f"({placeholders_pattern})", processed_text_for_display)

                # Helper to map placeholders back to their command strings
                placeholder_to_cmd_map = {cd["placeholder"]: cd["command_str"] for cd in command_details}

                for part in filter(None, text_parts): # filter(None,...) removes empty strings if any
                    if part in placeholder_to_cmd_map:
                        # This part is a placeholder, so render a command block
                        cmd_str = placeholder_to_cmd_map[part]
                        
                        cmd_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
                        cmd_box.get_style_context().add_class("command-block") # Apply CSS

                        cmd_label = Gtk.Label()
                        # Format command with a '$' prefix and monospace font using Pango
                        cmd_label.set_markup(f'<span font_family="monospace" weight="bold">$ {cmd_str}</span>')
                        cmd_label.set_xalign(0)
                        cmd_box.pack_start(cmd_label, True, True, 0)

                        if not self.auto_run_switch.get_active():
                            # Add run button only if auto-run is off
                            button_widget = self.create_run_button(cmd_str)
                            cmd_box.pack_end(button_widget, False, False, 0)
                        
                        message_content_container.pack_start(cmd_box, False, False, 0)
                    else:
                        # This part is regular text
                        if part.strip(): # Avoid adding empty labels
                            label = Gtk.Label()
                            label.set_markup(part) # Use set_markup for any Pango in text segments
                            label.set_line_wrap(True)
                            label.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)
                            label.set_xalign(0)
                            message_content_container.pack_start(label, False, False, 0)
            
            message_box.add(message_content_container)
        else: # User message
            label = Gtk.Label(label=text_content)
            label.set_line_wrap(True)
            label.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)
            label.set_xalign(0)
            label.set_margin_start(12)
            label.set_margin_end(12)
            label.set_margin_top(8)
            label.set_margin_bottom(8)
            message_box.add(label)
        
        align.add(message_box)
        self.messages_box.pack_start(align, False, False, 0)
        align.show_all()
        
        # Auto scroll to bottom
        adj = self.messages_box.get_parent().get_vadjustment()
        def scroll_to_bottom():
            adj.set_value(adj.get_upper() - adj.get_page_size())
        GLib.idle_add(scroll_to_bottom)
    
    def add_user_message(self, text):
        self.add_message(text, "user")
    
    def add_assistant_message(self, text):
        # This is now just a wrapper, auto-run is handled by the caller
        self.add_message(text, "assistant")
    
    def on_entry_activate(self, widget):
        text = self.entry.get_text().strip()
        if not text:
            return # Do nothing if input is empty
            
        self.add_user_message(text)
        self.entry.set_text("")
        
        # Create async task for AI response and processing
        async def get_response_and_process():
            try:
                llm_response_text = await self.get_ai_response(text) # Original LLM response

                # This function will be called by GLib.idle_add, so it runs in the main GTK thread
                def do_gui_update_after_ai():
                    # Handle auto-run based on the original LLM response
                    if self.auto_run_switch.get_active():
                        commands_in_response = self.extract_commands(llm_response_text)
                        for cmd_to_run in commands_in_response:
                            self.execute_command(cmd_to_run)
                    
                    # Add assistant message to UI (it will be formatted for display by add_message)
                    self.add_assistant_message(llm_response_text)
                
                GLib.idle_add(do_gui_update_after_ai)
            
            except Exception as e:
                # Handle/display error if get_ai_response fails
                error_message = f"Error processing AI request: {str(e)}"
                GLib.idle_add(self.add_assistant_message, error_message)
        
        # Run the async task.
        # For Gtk, it's often better to run asyncio tasks in a way that integrates with GLib's main loop
        # or in a separate thread to avoid blocking. asyncio.run() can block.
        # However, if this was working before, we'll keep it for now to focus on display.
        # A more robust Gtk+asyncio integration might be needed for complex apps.
        asyncio.run(get_response_and_process())

def main():
    win = DeepShellWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    
    # Check if settings exist, if not show settings dialog
    if not win.settings.get('api_key'):
        win.on_settings_clicked(None)
    
    Gtk.main()

if __name__ == "__main__":
    main() 