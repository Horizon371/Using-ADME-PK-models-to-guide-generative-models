reinvent="/home/jovyan/cristian/Reinvent/input.py"
config_path="/home/jovyan/cristian/scripts/config.json"
output_dir="/home/jovyan/cristian/outputs"

source /home/jovyan/miniconda3/bin/activate reinvent.v3.2

echo $config_path
python reinvent_config.py $output_dir $config_path
python $reinvent $config_path > $output_dir/err.log
#python print_results.py $output_dir/err.log