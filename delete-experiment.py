# delete experiment
import boto3

EXPERIMENT_NAME = '<EXPERIMENT NAME>' # Experiment name
MAX_RESULTS = 100 # Number of result retrieve in listing
TRY_NUM = 10 # Number of try

client = boto3.client('sagemaker')

def delete_experiment(experiment_name, max_results):
    while True:
        # Get trial list
        trial_list = client.list_trials(
            ExperimentName=experiment_name,
            MaxResults=max_results,
        )
        trial_num = len(trial_list['TrialSummaries'])

        # Ends if there are no more trials
        if trial_num == 0:
            break

        print("Info: Number of trials left: Over {}".format(trial_num))
        # Get trial component list
        for trial in trial_list['TrialSummaries']:
            trial_name = trial['TrialName']
            trial_component_list = client.list_trial_components(
                TrialName=trial_name,
                MaxResults=max_results,
            )

            # Disassociate trial component
            for trial_component in trial_component_list['TrialComponentSummaries']:
                trial_component_name = trial_component['TrialComponentName']
                response = client.disassociate_trial_component(
                    TrialComponentName=trial_component_name,
                    TrialName=trial_name
                )

            # Delete trial
            client.delete_trial(
                TrialName=trial_name
            )
            print("Info: Trial deleted. [{}]".format(trial_name))

    # Delete Experiment
    client.delete_experiment(
        ExperimentName=experiment_name
    )
    print("Info: Experiment deleted. [{}]".format(experiment_name))


for i in range(1, TRY_NUM + 1):
    try:
        # Delete if experiment exists
        experiment_list_all = client.list_experiments(
            MaxResults = MAX_RESULTS
        )
        experiment_name_list = [experiment['ExperimentName'] for experiment in experiment_list_all['ExperimentSummaries']]
        if EXPERIMENT_NAME in experiment_name_list:
            delete_experiment(EXPERIMENT_NAME, MAX_RESULTS)
    except Exception as e:
        print("Error: {}".format(e))
        print("Try: {i}/{max}".format(i=i, max=TRY_NUM))
    except Exception as e:
        print(e)
print("finish")