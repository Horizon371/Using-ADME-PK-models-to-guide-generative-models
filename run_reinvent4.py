import subprocess

reinvent = "/home/jovyan/cristian/REINVENT4/reinvent/Reinvent.py"
config_path = "/home/jovyan/cristian/scripts/transfer_learning.toml"
output_path = "/home/jovyan/cristian/outputs/transfer_learning_25/reinvent4_v2_stereo_TL_run.log"

subprocess.run(["python3", reinvent, "-l", output_path, config_path])
