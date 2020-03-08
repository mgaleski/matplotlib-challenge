import matplotlib.pyplot as plt
import pandas as pd

mouse_data = pd.read_csv('./data/Mouse_metadata.csv')
study_results = pd.read_csv('./data/Study_results.csv')

print(mouse_data.head())
print(study_results.head())
study_results.set_index(['Mouse ID'])
print(study_results.head())

regimens = mouse_data['Drug Regimen'].unique()

tumors = {}
tumors['Mouse ID'] = study_results['Mouse ID']
tumors['Volume'] = study_results['Tumor Volume (mm3)']
tumors = pd.DataFrame(tumors)

mouse_data = mouse_data.set_index('Mouse ID').join(tumors.set_index('Mouse ID'))
mouse_data = mouse_data.reset_index()

tumor_data = mouse_data.drop(columns=['Sex', 'Mouse ID', 'Age_months', 'Weight (g)'])
regimens = pd.DataFrame(mouse_data['Drug Regimen'].unique())

regimen_data = mouse_data.groupby(['Drug Regimen']).mean()
regimen_data['# of subjects'] = mouse_data['Drug Regimen'].value_counts()
regimen_data = regimen_data.reset_index()
print(mouse_data.head())

tumor_data_stdev = tumor_data.groupby(['Drug Regimen']).std()


stdevs = []
for value in range(10):
    stdevs.append(tumor_data_stdev['Volume'][value])
chart_mouse_id = 's185'


regimen_data['stdev'] = stdevs

bar_chart_data = regimen_data.drop(columns=['Age_months','Weight (g)', 'Volume'])
capomulin_data = mouse_data[mouse_data['Drug Regimen'] == 'Capomulin']

line_chart_data = study_results[study_results['Mouse ID'] == chart_mouse_id]
line_chart_x = line_chart_data['Timepoint']
line_chart_y = line_chart_data['Tumor Volume (mm3)']

scatter_data = capomulin_data.groupby(['Mouse ID']).mean()
scatter_data = scatter_data.reset_index()
scatter_x = scatter_data['Weight (g)']
scatter_y = scatter_data['Volume']

fig, a = plt.subplots(2,2)
sex_counts = mouse_data['Sex'].value_counts()
pie_labels = ['Male', 'Female']

a[0][0].bar(bar_chart_data['Drug Regimen'], bar_chart_data['# of subjects'])
a[0][0].set_xlabel('Drug Regimen')
a[0][0].set_ylabel('# of cases')
a[0][0].set_title('Drug Comparison')

a[0][1].pie(sex_counts, labels=pie_labels)
a[0][1].set_title('Sex breakdown')

a[1][1] = bar_chart_data.plot(kind='bar')

fig = plt.figure()
line_chart = fig.add_subplot(1,1,1)
line_chart.plot(line_chart_x,line_chart_y,marker='o',)
line_chart.set_title('Tumor volume over time in S185', fontsize = 20)
line_chart.set_xlabel('Timepoint')
line_chart.set_ylabel('Tumor Volume (mm3)')
line_chart.set_title('Tumor Volume over time in Subject S185 (Capomulin)')

fig2 = plt.figure()
scatter_chart = fig2.add_subplot(1,1,1)
scatter_chart.scatter(scatter_x, scatter_y)
scatter_chart.set_title('Mouse Weight vs. Tumor Volume')
scatter_chart.set_xlabel('Weight (g)')
scatter_chart.set_ylabel('Volume (mm3)')
plt.show()




