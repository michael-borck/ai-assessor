import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

from ...utils.document_processor import DocumentProcessor


class ConfigView(ttk.Frame):
    """
    Configuration tab of the application.
    """

    def __init__(self, parent, config_manager, string_vars, available_models=None, master_gui=None):
        """
        Initialize the configuration view.

        Args:
            parent: The parent widget
            config_manager: The configuration manager
            string_vars: Dictionary of StringVar objects for configuration
            available_models: List of available models from the LLM provider (optional)
        """
        super().__init__(parent)
        self.config_manager = config_manager
        self.string_vars = string_vars
        self.document_processor = DocumentProcessor()
        self.available_models = available_models or []
        self.ssl_verify_var = tk.BooleanVar(
            value=self.config_manager.get_value("API", "SSLVerify", "True").lower()
            == "true"
        )
        self.master_gui = master_gui

        # Setup UI
        self.setup_ui()

        # Bind API-related StringVars to update the API client
        self.string_vars["api_key"].trace_add("write", self._on_api_setting_change)
        self.string_vars["base_url"].trace_add("write", self._on_api_setting_change)
        self.ssl_verify_var.trace_add("write", self._on_api_setting_change)
        self.string_vars["model"].trace_add("write", self._on_api_setting_change)
        self.string_vars["temperature"].trace_add("write", self._on_api_setting_change)

    def _on_api_setting_change(self, *args):
        """Callback for when an API-related setting changes."""
        # Update config_manager with the new values
        self.config_manager.set_value("API", "Key", self.string_vars["api_key"].get())
        self.config_manager.set_value("API", "BaseURL", self.string_vars["base_url"].get())
        self.config_manager.set_value("API", "SSLVerify", self.ssl_verify_var.get())
        self.config_manager.set_value("API", "DefaultModel", self.string_vars["model"].get())
        self.config_manager.set_value("API", "Temperature", self.string_vars["temperature"].get())

        if self.master_gui:
            self.master_gui.update_api_client_settings()

    def setup_ui(self):
        """Set up the UI elements for the configuration tab."""
        # Configure grid layout
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        # API Configuration
        row = 0
        ttk.Label(self, text="API Key:").grid(
            row=row, column=0, sticky="w", padx=5, pady=5
        )
        ttk.Entry(self, textvariable=self.string_vars["api_key"]).grid(
            row=row, column=1, sticky="ew", padx=5, pady=5
        )

        row += 1
        ttk.Label(self, text="Base URL (required):").grid(
            row=row, column=0, sticky="w", padx=5, pady=5
        )
        base_url_frame = ttk.Frame(self)
        base_url_frame.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
        ttk.Entry(base_url_frame, textvariable=self.string_vars["base_url"]).pack(
            side="top", fill="x", expand=True
        )

        # Add examples label
        examples_text = "Examples: https://api.openai.com (OpenAI) | http://localhost:11434 (Ollama)"
        ttk.Label(
            base_url_frame, text=examples_text, font=("Helvetica", 8), foreground="gray"
        ).pack(side="top", anchor="w", pady=(2, 0))

        row += 1
        ttk.Checkbutton(
            self, text="Verify SSL Certificates", variable=self.ssl_verify_var
        ).grid(row=row, column=0, columnspan=2, sticky="w", padx=5, pady=5)

        # Path Configuration
        row += 1
        ttk.Label(self, text="System Prompt File:").grid(
            row=row, column=0, sticky="w", padx=5, pady=5
        )
        path_frame = ttk.Frame(self)
        path_frame.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
        ttk.Entry(path_frame, textvariable=self.string_vars["system_prompt_path"]).pack(
            side="left", fill="x", expand=True
        )
        ttk.Button(
            path_frame,
            text="Browse",
            command=lambda: self.browse_file(
                "System Prompt", self.string_vars["system_prompt_path"]
            ),
        ).pack(side="right")

        row += 1
        ttk.Label(self, text="User Prompt File:").grid(
            row=row, column=0, sticky="w", padx=5, pady=5
        )
        path_frame = ttk.Frame(self)
        path_frame.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
        ttk.Entry(path_frame, textvariable=self.string_vars["user_prompt_path"]).pack(
            side="left", fill="x", expand=True
        )
        ttk.Button(
            path_frame,
            text="Browse",
            command=lambda: self.browse_file(
                "User Prompt", self.string_vars["user_prompt_path"]
            ),
        ).pack(side="right")

        row += 1
        ttk.Label(self, text="Support Files Folder:").grid(
            row=row, column=0, sticky="w", padx=5, pady=5
        )
        path_frame = ttk.Frame(self)
        path_frame.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
        ttk.Entry(path_frame, textvariable=self.string_vars["support_folder"]).pack(
            side="left", fill="x", expand=True
        )
        ttk.Button(
            path_frame,
            text="Browse",
            command=lambda: self.browse_directory(
                "Support Files", self.string_vars["support_folder"]
            ),
        ).pack(side="right")

        row += 1
        ttk.Label(self, text="Submissions Folder:").grid(
            row=row, column=0, sticky="w", padx=5, pady=5
        )
        path_frame = ttk.Frame(self)
        path_frame.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
        ttk.Entry(path_frame, textvariable=self.string_vars["submissions_folder"]).pack(
            side="left", fill="x", expand=True
        )
        ttk.Button(
            path_frame,
            text="Browse",
            command=lambda: self.browse_directory(
                "Submissions", self.string_vars["submissions_folder"]
            ),
        ).pack(side="right")

        row += 1
        ttk.Label(self, text="Output Folder:").grid(
            row=row, column=0, sticky="w", padx=5, pady=5
        )
        path_frame = ttk.Frame(self)
        path_frame.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
        ttk.Entry(path_frame, textvariable=self.string_vars["output_folder"]).pack(
            side="left", fill="x", expand=True
        )
        ttk.Button(
            path_frame,
            text="Browse",
            command=lambda: self.browse_directory(
                "Output", self.string_vars["output_folder"]
            ),
        ).pack(side="right")

        # Model Selection
        row += 1
        ttk.Label(self, text="Model:").grid(
            row=row, column=0, sticky="w", padx=5, pady=5
        )
        model_frame = ttk.Frame(self)
        model_frame.grid(row=row, column=1, sticky="ew", padx=5, pady=5)

        # Use available models if fetched, otherwise use config
        if self.available_models:
            model_options = self.available_models
        else:
            model_options = (
                list(self.config_manager.config["Models"].keys())
                if self.config_manager.config.has_section("Models")
                else ["gpt-3.5-turbo", "gpt-4-turbo", "gpt-4o"]
            )

        # Create combobox for model selection
        self.model_dropdown = ttk.Combobox(
            model_frame, textvariable=self.string_vars["model"], values=model_options
        )
        self.model_dropdown.pack(side="left", fill="x", expand=True)

        # Add button to test connection
        ttk.Button(
            model_frame, text="Test Connection", command=self.test_connection
        ).pack(side="right", padx=5)

        # Add button to refresh models
        ttk.Button(
            model_frame, text="Refresh Models", command=self.refresh_models
        ).pack(side="right", padx=5)

        # Add button to add new model
        ttk.Button(model_frame, text="Manage Models", command=self.manage_models).pack(
            side="right", padx=5
        )

        # Temperature Setting
        row += 1
        ttk.Label(self, text="Temperature (0-1):").grid(
            row=row, column=0, sticky="w", padx=5, pady=5
        )
        ttk.Entry(self, textvariable=self.string_vars["temperature"]).grid(
            row=row, column=1, sticky="w", padx=5, pady=5, ipadx=10
        )

        # System Prompt Editor
        row += 1
        ttk.Label(self, text="System Prompt:").grid(
            row=row, column=0, columnspan=2, sticky="w", padx=5, pady=5
        )

        row += 1
        self.system_prompt_editor = scrolledtext.ScrolledText(self, height=10)
        self.system_prompt_editor.grid(
            row=row, column=0, columnspan=2, sticky="ew", padx=5, pady=5
        )
        self.rowconfigure(row, weight=1)

        # Buttons for system prompt
        row += 1
        button_frame = ttk.Frame(self)
        button_frame.grid(row=row, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        ttk.Button(
            button_frame, text="Load System Prompt", command=self.load_system_prompt
        ).pack(side="left", padx=5)
        ttk.Button(
            button_frame, text="Save System Prompt", command=self.save_system_prompt
        ).pack(side="left", padx=5)

        # User Prompt Editor
        row += 1
        ttk.Label(self, text="User Prompt:").grid(
            row=row, column=0, columnspan=2, sticky="w", padx=5, pady=5
        )

        row += 1
        self.user_prompt_editor = scrolledtext.ScrolledText(self, height=10)
        self.user_prompt_editor.grid(
            row=row, column=0, columnspan=2, sticky="ew", padx=5, pady=5
        )
        self.rowconfigure(row, weight=1)

        # Buttons for user prompt
        row += 1
        button_frame = ttk.Frame(self)
        button_frame.grid(row=row, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        ttk.Button(
            button_frame, text="Load User Prompt", command=self.load_user_prompt
        ).pack(side="left", padx=5)
        ttk.Button(
            button_frame, text="Save User Prompt", command=self.save_user_prompt
        ).pack(side="left", padx=5)

        # Load prompts if paths are set
        self.load_initial_prompts()

    def browse_file(self, file_type, string_var):
        """
        Browse for a file and update the corresponding path.

        Args:
            file_type (str): Type of file to browse for
            string_var (StringVar): StringVar to update with the selected path
        """
        filename = filedialog.askopenfilename(
            title=f"Select {file_type} File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if filename:
            string_var.set(filename)

    def browse_directory(self, directory_type, string_var):
        """
        Browse for a directory and update the corresponding path.
        Creates the directory if it doesn't exist (with user confirmation).

        Args:
            directory_type (str): Type of directory to browse for
            string_var (StringVar): StringVar to update with the selected path
        """
        # For output folder, allow typing a new path
        if directory_type == "Output":
            # Start with current value if exists
            initial_dir = string_var.get() if string_var.get() else os.getcwd()

            # Use askdirectory which allows typing new paths
            directory = filedialog.askdirectory(
                title=f"Select or Create {directory_type} Directory",
                initialdir=(
                    os.path.dirname(initial_dir)
                    if os.path.exists(os.path.dirname(initial_dir))
                    else os.getcwd()
                ),
            )
        else:
            directory = filedialog.askdirectory(
                title=f"Select {directory_type} Directory"
            )

        if directory:
            # Check if directory exists
            if not os.path.exists(directory):
                # Ask user if they want to create it
                response = messagebox.askyesno(
                    "Create Directory",
                    f"The directory '{directory}' does not exist.\n\nWould you like to create it?",
                )

                if response:
                    try:
                        os.makedirs(directory, exist_ok=True)
                        string_var.set(directory)
                        messagebox.showinfo(
                            "Success", f"Directory created successfully:\n{directory}"
                        )
                    except Exception as e:
                        messagebox.showerror(
                            "Error", f"Failed to create directory:\n{str(e)}"
                        )
                # else: User chose not to create, don't update the path
            else:
                string_var.set(directory)

    def load_initial_prompts(self):
        """Load initial prompts if paths are set."""
        # Load system prompt
        system_prompt_path = self.string_vars["system_prompt_path"].get()
        if system_prompt_path and os.path.exists(system_prompt_path):
            try:
                content = self.document_processor.read_text_file(system_prompt_path)
                self.system_prompt_editor.delete(1.0, tk.END)
                self.system_prompt_editor.insert(tk.END, content)
            except Exception as e:
                print(f"Error loading system prompt: {e}")

        # Load user prompt
        user_prompt_path = self.string_vars["user_prompt_path"].get()
        if user_prompt_path and os.path.exists(user_prompt_path):
            try:
                content = self.document_processor.read_text_file(user_prompt_path)
                self.user_prompt_editor.delete(1.0, tk.END)
                self.user_prompt_editor.insert(tk.END, content)
            except Exception as e:
                print(f"Error loading user prompt: {e}")

    def load_system_prompt(self):
        """Load system prompt from the specified path."""
        path = self.string_vars["system_prompt_path"].get()
        if path and os.path.exists(path):
            try:
                content = self.document_processor.read_text_file(path)
                self.system_prompt_editor.delete(1.0, tk.END)
                self.system_prompt_editor.insert(tk.END, content)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load system prompt: {e}")
        else:
            messagebox.showwarning(
                "Warning", "Please specify a valid system prompt path."
            )

    def save_system_prompt(self):
        """Save system prompt to the specified path."""
        path = self.string_vars["system_prompt_path"].get()
        if path:
            try:
                content = self.system_prompt_editor.get(1.0, tk.END)
                self.document_processor.write_text_file(path, content)
                messagebox.showinfo("Success", "System prompt saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save system prompt: {e}")
        else:
            messagebox.showwarning("Warning", "Please specify a system prompt path.")

    def load_user_prompt(self):
        """Load user prompt from the specified path."""
        path = self.string_vars["user_prompt_path"].get()
        if path and os.path.exists(path):
            try:
                content = self.document_processor.read_text_file(path)
                self.user_prompt_editor.delete(1.0, tk.END)
                self.user_prompt_editor.insert(tk.END, content)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load user prompt: {e}")
        else:
            messagebox.showwarning(
                "Warning", "Please specify a valid user prompt path."
            )

    def save_user_prompt(self):
        """Save user prompt to the specified path."""
        path = self.string_vars["user_prompt_path"].get()
        if path:
            try:
                content = self.user_prompt_editor.get(1.0, tk.END)
                self.document_processor.write_text_file(path, content)
                messagebox.showinfo("Success", "User prompt saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save user prompt: {e}")
        else:
            messagebox.showwarning("Warning", "Please specify a user prompt path.")

    def test_connection(self):
        """Test the connection to the LLM provider and list available models."""
        api_key = self.string_vars["api_key"].get()
        base_url = self.string_vars["base_url"].get()
        ssl_verify = self.ssl_verify_var.get()

        print("--- Testing Connection ---")
        print(f"API Key: {api_key}")
        print(f"Base URL: {base_url}")
        print(f"SSL Verify: {ssl_verify}")
        print("--------------------------")

        # Validate required fields
        if not api_key:
            messagebox.showerror("Error", "API Key is required.")
            return

        if not base_url or base_url.strip() == "":
            messagebox.showerror(
                "Error",
                "Base URL is required.\n\nExamples:\n"
                + "• OpenAI: https://api.openai.com\n"
                + "• Ollama: http://localhost:11434\n"
                + "• LM Studio: http://localhost:1234",
            )
            return

        from ...core.api_client import OpenAIClient

        try:
            client = OpenAIClient(
                api_key=api_key, base_url=base_url, ssl_verify=ssl_verify
            )
            models = client.list_models()
            model_ids = [model.id for model in models.data]
            messagebox.showinfo(
                "Connection Successful",
                f"Successfully connected to the provider. Found {len(model_ids)} models:\n\n"
                + "\n".join(model_ids),
            )
        except ValueError as e:
            # Handle validation errors (missing API key/base URL)
            messagebox.showerror("Configuration Error", str(e))
        except Exception as e:
            import traceback

            print(traceback.format_exc())
            messagebox.showerror(
                "Connection Failed",
                f"Failed to connect to the provider:\n\n{str(e)}\n\nPlease check:\n"
                + "• Base URL is correct and accessible\n"
                + "• API key is valid\n"
                + "• Network connectivity",
            )

    def refresh_models(self):
        """Refresh available models from the LLM provider."""
        api_key = self.string_vars["api_key"].get()
        base_url = self.string_vars["base_url"].get()
        ssl_verify = self.ssl_verify_var.get()
        # Validate required fields
        if not api_key:
            messagebox.showerror("Error", "API Key is required.")
            return

        if not base_url or base_url.strip() == "":
            messagebox.showerror(
                "Error",
                "Base URL is required.\n\nExamples:\n"
                + "• OpenAI: https://api.openai.com\n"
                + "• Ollama: http://localhost:11434\n"
                + "• LM Studio: http://localhost:1234",
            )
            return

        from ...core.api_client import OpenAIClient

        try:
            client = OpenAIClient(
                api_key=api_key, base_url=base_url, ssl_verify=ssl_verify
            )
            models = client.list_models()
            # Include all models from the provider, not just those matching specific patterns
            # This allows for custom/local models with any naming convention
            all_models = [model.id for model in models.data]
            self.available_models = sorted(all_models) if all_models else []
            self.model_dropdown["values"] = self.available_models

            if self.available_models:
                # Save models to config.ini
                if self.config_manager.config.has_section("Models"):
                    self.config_manager.config.remove_section("Models")
                self.config_manager.config.add_section("Models")
                for model_id in self.available_models:
                    self.config_manager.set_value("Models", model_id, model_id)
                self.config_manager.save()

                messagebox.showinfo(
                    "Models Updated",
                    f"Found {len(self.available_models)} available models.",
                )
            else:
                messagebox.showwarning(
                    "No Models Found",
                    "No compatible models were found. Using default models.",
                )
        except ValueError as e:
            # Handle validation errors (missing API key/base URL)
            messagebox.showerror("Configuration Error", str(e))
        except Exception as e:
            import traceback

            print(traceback.format_exc())
            messagebox.showerror(
                "Connection Failed",
                f"Failed to connect to the provider:\n\n{str(e)}\n\nPlease check:\n"
                + "• Base URL is correct and accessible\n"
                + "• API key is valid\n"
                + "• Network connectivity",
            )

    def _update_model_dropdown(self, loading_dialog):
        """Update model dropdown with fetched models."""
        try:
            # Check if dialog still exists before trying to destroy it
            if loading_dialog.winfo_exists():
                if self.available_models:
                    # Update dropdown
                    self.model_dropdown["values"] = self.available_models

                    # Close loading dialog
                    loading_dialog.destroy()

                    # Show success message
                    messagebox.showinfo(
                        "Models Updated",
                        f"Found {len(self.available_models)} available models.\n"
                        f"These models have been saved to your configuration.",
                    )

                    # Refresh manage models dialog if it's open
                    for widget in self.winfo_toplevel().winfo_children():
                        if (
                            isinstance(widget, tk.Toplevel)
                            and widget.title() == "Manage Models"
                        ):
                            # There's an open Manage Models dialog - refresh it
                            try:
                                # Find the listbox in the dialog
                                for child in widget.winfo_children():
                                    listbox = self._find_listbox_in_widget(child)
                                    if listbox:
                                        # Refresh the listbox
                                        listbox.delete(0, tk.END)
                                        for model_name in self.config_manager.config[
                                            "Models"
                                        ].keys():
                                            listbox.insert(tk.END, model_name)
                                        break
                            except Exception:
                                # If anything goes wrong, don't worry - user can close and reopen
                                pass
                else:
                    loading_dialog.destroy()
                    messagebox.showwarning(
                        "No Models Found",
                        "No compatible models were found. Using default models.",
                    )
                    self.model_dropdown["values"] = [
                        "gpt-4-turbo",
                        "gpt-4o",
                        "gpt-3.5-turbo",
                    ]
            else:
                # Dialog was already closed (e.g., by user or timeout)
                if self.available_models:
                    self.model_dropdown["values"] = self.available_models
                else:
                    self.model_dropdown["values"] = [
                        "gpt-4-turbo",
                        "gpt-4o",
                        "gpt-3.5-turbo",
                    ]
        except Exception:
            # Handle any unexpected errors
            self.model_dropdown["values"] = ["gpt-4-turbo", "gpt-4o", "gpt-3.5-turbo"]

    def _find_listbox_in_widget(self, widget):
        """Recursively search for a Listbox widget in children."""
        if isinstance(widget, tk.Listbox):
            return widget

        # Check all children
        if hasattr(widget, "winfo_children"):
            for child in widget.winfo_children():
                result = self._find_listbox_in_widget(child)
                if result:
                    return result

        return None

    def _handle_refresh_error(self, error, loading_dialog):
        """Handle errors when refreshing models."""
        try:
            # Check if dialog still exists before trying to destroy it
            if loading_dialog.winfo_exists():
                loading_dialog.destroy()

            # Show error message
            messagebox.showerror("Error", f"Failed to fetch models: {str(error)}")

            # Fall back to default models
            self.model_dropdown["values"] = ["gpt-4-turbo", "gpt-4o", "gpt-3.5-turbo"]
        except Exception:
            # Dialog was already destroyed or other error
            pass

    def manage_models(self):
        """Open dialog to manage models."""
        # Create a new dialog window
        dialog = tk.Toplevel(self)
        dialog.title("Manage Models")
        dialog.geometry("500x480")
        dialog.transient(self)  # Make dialog modal
        dialog.grab_set()  # Make dialog modal

        # Create a frame for the model list
        frame = ttk.Frame(dialog, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # Description label
        description = (
            "Manage the available models for AI Assessor.\n\n"
            "You can add custom models, remove models you don't use, "
            "or use 'Refresh Models' button to fetch the latest models from your provider."
        )
        ttk.Label(frame, text=description, wraplength=480).grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 15)
        )

        # Create a model list with scrollbar
        list_frame = ttk.Frame(frame)
        list_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=5)

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a listbox with current models
        model_listbox = tk.Listbox(
            list_frame, yscrollcommand=scrollbar.set, height=10, font=("Helvetica", 10)
        )
        model_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=model_listbox.yview)

        # Populate the listbox with current models
        if self.config_manager.config.has_section("Models"):
            for model_name in self.config_manager.config["Models"].keys():
                model_listbox.insert(tk.END, model_name)

        # Frame for model management buttons
        buttons_frame = ttk.Frame(frame)
        buttons_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)

        # Refresh button to update models from provider
        ttk.Button(
            buttons_frame,
            text="Refresh Models from Provider",
            command=lambda: self._refresh_from_manage_dialog(dialog),
        ).pack(side=tk.LEFT, padx=5)

        # Remove button
        ttk.Button(
            buttons_frame,
            text="Remove Selected",
            command=lambda: self._remove_model(model_listbox),
        ).pack(side=tk.LEFT, padx=5)

        # Separator
        ttk.Separator(frame, orient="horizontal").grid(
            row=3, column=0, columnspan=2, sticky="ew", pady=15
        )

        # Add custom model section
        ttk.Label(frame, text="Add Custom Model", font=("Helvetica", 10, "bold")).grid(
            row=4, column=0, columnspan=2, sticky="w", pady=(0, 10)
        )

        # Frame for new model addition
        add_frame = ttk.Frame(frame)
        add_frame.grid(row=5, column=0, columnspan=2, sticky="ew", pady=5)

        ttk.Label(add_frame, text="Model Name:").grid(
            row=0, column=0, sticky="w", padx=5, pady=5
        )
        model_name_var = tk.StringVar()
        model_name_entry = ttk.Entry(add_frame, textvariable=model_name_var)
        model_name_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(add_frame, text="Model ID:").grid(
            row=1, column=0, sticky="w", padx=5, pady=5
        )
        model_id_var = tk.StringVar()
        model_id_entry = ttk.Entry(add_frame, textvariable=model_id_var)
        model_id_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(
            add_frame,
            text="Note: For most models, Name and ID are the same value (e.g., 'gpt-4-turbo')",
            font=("Helvetica", 9),
            foreground="gray",
        ).grid(row=2, column=0, columnspan=2, sticky="w", padx=5, pady=5)

        # Frame for add and close buttons
        action_buttons = ttk.Frame(frame)
        action_buttons.grid(row=6, column=0, columnspan=2, sticky="ew", pady=10)

        # Add model function
        def add_model():
            name = model_name_var.get().strip()
            model_id = model_id_var.get().strip()

            if not name or not model_id:
                messagebox.showwarning(
                    "Warning", "Please enter both a model name and ID."
                )
                return

            # Add to config
            if not self.config_manager.config.has_section("Models"):
                self.config_manager.config.add_section("Models")

            self.config_manager.set_value("Models", name, model_id)
            self.config_manager.save()

            # Add to listbox
            model_listbox.insert(tk.END, name)

            # Clear entries
            model_name_var.set("")
            model_id_var.set("")

            # Update dropdown in main view
            self.model_dropdown["values"] = list(
                self.config_manager.config["Models"].keys()
            )

            messagebox.showinfo("Success", f"Added model: {name}")

        ttk.Button(action_buttons, text="Add Custom Model", command=add_model).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(action_buttons, text="Close", command=dialog.destroy).pack(
            side=tk.RIGHT, padx=5
        )

        # Configure grid weights
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(1, weight=1)

        # Make dialog modal
        dialog.wait_window()

    def _refresh_from_manage_dialog(self, parent_dialog):
        """Refresh models from within the manage models dialog."""
        # Hide the manage dialog temporarily
        parent_dialog.withdraw()

        # Call the regular refresh function
        self.refresh_models()

        # Show the manage dialog again after a short delay
        self.winfo_toplevel().after(500, parent_dialog.deiconify)

    def _remove_model(self, model_listbox):
        """Remove a model from the listbox and config."""
        # Get selected model
        selected = model_listbox.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a model to remove.")
            return

        model_name = model_listbox.get(selected[0])

        # Confirm removal
        if messagebox.askyesno(
            "Confirm", f"Are you sure you want to remove {model_name}?"
        ):
            # Remove from config
            if self.config_manager.config.has_option("Models", model_name):
                self.config_manager.config.remove_option("Models", model_name)
                self.config_manager.save()

            # Remove from listbox
            model_listbox.delete(selected[0])

            # Update dropdown in main view
            self.model_dropdown["values"] = list(
                self.config_manager.config["Models"].keys()
            )

            messagebox.showinfo("Success", f"Removed model: {model_name}")
