#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Vte', '2.91')
from gi.repository import Gtk, Gdk, GLib, Pango, Vte
import os

class DeepShellWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Deep Shell")
        
        # Set up window properties
        self.set_default_size(1200, 700)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        # Enable transparency
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual and screen.is_composited():
            self.set_visual(visual)
        
        # Set up CSS provider
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path("style.css")
        Gtk.StyleContext.add_provider_for_screen(
            screen,
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        
        # Main horizontal container
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.add(self.main_box)
        
        # Left panel for chat interface
        self.chat_panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.chat_panel.set_size_request(600, -1)  # Set minimum width for chat panel
        self.main_box.pack_start(self.chat_panel, True, True, 0)
        
        # Header bar
        self.header = Gtk.HeaderBar()
        self.header.set_show_close_button(True)
        self.header.props.title = "Deep Shell"
        self.set_titlebar(self.header)
        
        # Logo and title in header
        logo_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        logo_image = Gtk.Image.new_from_icon_name("utilities-terminal", Gtk.IconSize.LARGE_TOOLBAR)
        logo_box.pack_start(logo_image, False, False, 0)
        self.header.pack_start(logo_box)
        
        # Settings and reset buttons
        settings_button = Gtk.Button()
        settings_icon = Gtk.Image.new_from_icon_name("preferences-system", Gtk.IconSize.BUTTON)
        settings_button.add(settings_icon)
        settings_button.get_style_context().add_class("header-button")
        
        reset_button = Gtk.Button()
        reset_icon = Gtk.Image.new_from_icon_name("view-refresh", Gtk.IconSize.BUTTON)
        reset_button.add(reset_icon)
        reset_button.get_style_context().add_class("header-button")
        
        self.header.pack_end(settings_button)
        self.header.pack_end(reset_button)
        
        # Messages ScrolledWindow
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
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
        input_box.set_margin_start(16)
        input_box.set_margin_end(16)
        input_box.set_margin_top(8)
        input_box.set_margin_bottom(16)
        self.chat_panel.pack_end(input_box, False, False, 0)
        
        # Text input
        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Ask me anything about the terminal...")
        self.entry.connect("activate", self.on_entry_activate)
        input_box.pack_start(self.entry, True, True, 0)
        
        # Send button
        send_button = Gtk.Button()
        send_icon = Gtk.Image.new_from_icon_name("send", Gtk.IconSize.BUTTON)
        send_button.add(send_icon)
        send_button.connect("clicked", self.on_entry_activate)
        send_button.get_style_context().add_class("send-button")
        input_box.pack_end(send_button, False, False, 0)
        
        # Separator between chat and terminal
        separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        separator.get_style_context().add_class("panel-separator")
        self.main_box.pack_start(separator, False, False, 0)
        
        # Right panel for terminal
        self.terminal_panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.terminal_panel.set_size_request(600, -1)  # Set minimum width for terminal panel
        self.main_box.pack_start(self.terminal_panel, True, True, 0)
        
        # Create terminal
        self.terminal = Vte.Terminal()
        self.terminal.set_cursor_blink_mode(Vte.CursorBlinkMode.ON)
        self.terminal.set_cursor_shape(Vte.CursorShape.IBEAM)
        
        # Set terminal opacity
        self.terminal.set_color_background(Gdk.RGBA(0.1, 0.1, 0.1, 0.95))  # 95% opacity
        self.terminal.set_color_foreground(Gdk.RGBA(0.9, 0.9, 0.9, 1.0))
        
        # Enable transparency
        self.terminal.set_clear_background(False)
        
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
        
        # Set up styles
        self.get_style_context().add_class("deep-shell-window")
        scrolled.get_style_context().add_class("messages-scroll")
        self.messages_box.get_style_context().add_class("messages-container")
        input_box.get_style_context().add_class("input-container")
        self.entry.get_style_context().add_class("message-input")
        self.terminal.get_style_context().add_class("terminal-widget")
        
    def add_message(self, text, message_type):
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
        
        # Label
        label = Gtk.Label(label=text)
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
        self.add_message(text, "assistant")
    
    def on_entry_activate(self, widget):
        text = self.entry.get_text().strip()
        if text:
            self.add_user_message(text)
            self.entry.set_text("")
            # Simulate assistant response
            GLib.timeout_add(1000, self.simulate_response, text)
    
    def simulate_response(self, user_text):
        self.add_assistant_message(f"You said: {user_text}\nThis is a simulated response.")
        return False

def main():
    win = DeepShellWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main() 