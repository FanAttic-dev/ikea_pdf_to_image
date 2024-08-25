arch -x86_64 zsh
source .venv_x86_64/bin/activate
pyinstaller --name="IKEA_PDF_to_image" --onefile --windowed app_gui.py  