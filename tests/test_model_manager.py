from core.model_manager import ModelManager

manager = ModelManager()

print("Models Folder:")

print(manager.models_directory)

print()

print("Available Models:")

print(manager.list_models())