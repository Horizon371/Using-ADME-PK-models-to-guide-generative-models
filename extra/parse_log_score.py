import statistics


def parse_reinvent_logs_for_final_score(logging_path):
    results = get_results(logging_path, "<INFO> Score")
    print(statistics.mean(results))

def get_results(file_path, substring):
    scores = []
    with open(file_path, 'r') as file:
        for line in file:
            if substring in line:
                scores.append(float(line.strip().split(" ")[3]))
    return scores


parse_reinvent_logs_for_final_score("/home/jovyan/cristian/outputs/drd2_1_div_ScaffoldSimiliarty_v25p/drd2_1_div_ScaffoldSimiliarty_v25p_run.log")