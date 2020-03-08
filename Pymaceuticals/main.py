import matplotlib.pyplot as plt
import pandas as pd

mouse_data = pd.read_csv('./data/Mouse_metadata.csv')
study_results = pd.read_csv('./data/Study_results.csv')


regimens = mouse_data['Drug Regimen'].unique()

tumors = {}
tumors['Mouse ID'] = study_results['Mouse ID']
tumors['Volume'] = study_results['Tumor Volume (mm3)']
tumors = pd.DataFrame(tumors)
print(study_results)

mouse_data = mouse_data.set_index('Mouse ID').join(tumors.set_index('Mouse ID'))
mouse_data = mouse_data.reset_index()

tumor_data = mouse_data.drop(columns=['Sex', 'Mouse ID', 'Age_months', 'Weight (g)'])
regimens = pd.DataFrame(mouse_data['Drug Regimen'].unique())

regimen_data = mouse_data.groupby(['Drug Regimen']).mean()
regimen_data['# of subjects'] = mouse_data['Drug Regimen'].value_counts()
regimen_data = regimen_data.reset_index()


bar_chart_data = regimen_data.drop(columns=['Age_months','Weight (g)', 'Volume'])

tumor_data = tumor_data.groupby(['Drug Regimen']).std()
print(tumor_data)

print(tumor_data.groupby('Drug Regimen'))


sex_counts = mouse_data['Sex'].value_counts()
pie_labels = ['Male', 'Female']


fig, a = plt.subplots(2,2)

a[0][0].bar(bar_chart_data['Drug Regimen'], bar_chart_data['# of subjects'])
a[0][0].set_xlabel('Drug Regimen')
a[0][0].set_ylabel('# of cases')
a[0][0].set_title('Drug Comparison')

a[0][1].pie(sex_counts, labels=pie_labels)
a[0][1].set_title('Sex breakdown')

a[1][1] = bar_chart_data.plot(kind='bar')



plt.show()