####################################################################################################################
#General Information
####################################################################################################################
#
#
#
#
#   1. run the Data Preparation Section the first time you open the model; for future runs set a hashtag before the lines of code to decrease running time substantially
#
#   2. if your Scenario ends with '_V' and a number, change it to '_VX' in the script when running the function to get the latest version
#        - e.g.  create_heatmap_std('2080', 'NPi2020_1000_V2', 'World', variables_to_compare) will become create_heatmap_std('2080', 'NPi2020_1000_VX', 'World', variables_to_compare)
#        - if you do not want to update to the latest functions do not run the 'update_models()' function
#
#   3. You have to fill in the 'Newest Version' Table with the newest version if you would like the model to be included
#
#
#
#
                   


####################################################################################################################
#Defining function
####################################################################################################################




#returns row of the input table filtered through variable, region, scenario and model.
#possible inputs are the names of the table or 'all' to receive all
def getrow(variable, region, scenario, model):

    #selects based on row values
    selection = table_1.loc[
                ((variable == 'all') | (table_1['VARIABLE'] == variable))
                & ((region == 'all') | (table_1['REGION'] == region))
                & ((scenario == 'all') | (table_1['SCENARIO'] == scenario))
                & ((model == 'all') | (table_1['MODEL'] == model))
            ]
    if selection.empty: print('No data matches your criteria')

    return selection



#returns the wanted row but with only the cell value of the wanted year instead of all years
def getyear(variable, region, scenario, model, year):

    get_year = getrow(variable, region, scenario, model)
    return get_year.loc[:,['MODEL','SCENARIO','REGION','VARIABLE','UNIT', year]]

#returns 'clean' data, so it can be easier used
def get_clean_data(variable, region, scenario, model):
    table_2 = getrow(variable, region, scenario, model)
    table_2 = table_2.reset_index(drop=True)
    table_2 = table_2.drop(['REGION', 'UNIT', 'SCENARIO'], axis = 1)
    table_2 = table_2.dropna(axis = 1)
    return table_2

def get_clean_data_linegraph(variable, region, scenario, model):
    table_2 = getrow(variable, region, scenario, model)
    table_2 = table_2.reset_index(drop=True)
    table_2 = table_2.drop(['REGION', 'UNIT', 'SCENARIO'], axis = 1)
    table_2 = table_2.dropna(axis = 1)
    return table_2

def get_clean_data_linegraph_explicit(variable, region, scenario, model):
    table_2 = getrow(variable, region, scenario, model)
    table_2 = table_2.reset_index(drop=True)
    table_2 = table_2.drop(['REGION', 'UNIT', 'SCENARIO'], axis = 1)
    years = ['2010','2020','2030','2040','2050','2060','2070','2080','2090','2100']
    table_2 = table_2[years]
    return table_2



#returns data in way easily used for heat map
def data_prep_heat_map(year, scenario, region, variable_list):

    #get empty data frame for the for loop below
    model = 'all'
    heat_map_original_values = getyear(variable_list[0], region, scenario, model, year)
    del heat_map_original_values[year]
    heat_map_original_values = heat_map_original_values.set_index(heat_map_original_values.loc[:,'MODEL'])
    heat_map_original_values = heat_map_original_values.drop(['SCENARIO', 'REGION', 'VARIABLE', 'UNIT', 'MODEL'], axis = 1)
    
    
    #insert data for several variables into dataframe
    for name_data in variable_list:
        new_data = getyear(name_data, region, scenario, model, year)
        heat_map_original_values = fusematrix(new_data, heat_map_original_values, name_data)

    return heat_map_original_values


#creates line graph
def create_line_graph_2050(variable, region, scenario, model):
    
    #get data for labeling
    graph_labeler = getrow(variable, region, scenario, model)
    if graph_labeler.empty: return
    title = graph_labeler.iloc[0]['VARIABLE'] + ' | ' + graph_labeler.iloc[0]['REGION'] + ' | ' + graph_labeler.iloc[0]['SCENARIO']
    y_axis = graph_labeler.iloc[0]['UNIT']
    #get data for the graph
    graph_1 = get_clean_data_linegraph(variable, region, scenario, model)
    graph_1 = drop_unwanted_models(graph_1)
    if 'Scenarios original version name' in graph_1.columns:
        graph_1 = graph_1.drop(['MODEL', 'VARIABLE', 'Scenarios original version name'], axis = 1)
    else:
        graph_1 = graph_1.drop(['MODEL', 'VARIABLE'], axis = 1)
        
    #to only get 2050, uncomment next line
    #graph_1 = graph_1.drop(['2060','2070','2080','2090','2100'], axis = 1)    
    #plot the graph
    for i, row in graph_1.iterrows():
        plt.plot(row.index, row.values, label = graph_labeler.iloc[i]['MODEL'])
        
    #show the graph
    
    plt.title(title)
    plt.ylabel(y_axis)
    plt.xlabel('Years')
    plt.legend()
    plt.legend(bbox_to_anchor=(1.1, 1.05))
    name_of_fig = saving_location + 'line graph of ' + variable.replace('|', ' ') + ' of scenario ' + scenario + ' in ' + region +'.png'
    plt.savefig(name_of_fig, bbox_inches='tight')
    plt.show()
    


    
#creates line graph
def create_line_graph_explicit_2010_2100(variable, region, scenario, model):
    
    #get data for labeling
    graph_labeler = getrow(variable, region, scenario, model)
    title = graph_labeler.iloc[0]['VARIABLE'] + ' | ' + graph_labeler.iloc[0]['REGION'] + ' | ' + graph_labeler.iloc[0]['SCENARIO']
    y_axis = graph_labeler.iloc[0]['UNIT']
    #get data for the graph
    graph_1 = get_clean_data_linegraph_explicit(variable, region, scenario, model)
    #plot the graph
    for i, row in graph_1.iterrows():
        plt.plot(row.index, row.values, label = graph_labeler.iloc[i]['MODEL'])
        
    #show the graph
    plt.title(title)
    plt.ylabel(y_axis)
    plt.xlabel('Years')
    plt.legend()
    plt.legend(bbox_to_anchor=(1.1, 1.05))
    name_of_fig = saving_location + 'line graph of ' + variable.replace('|', ' ') + ' of scenario ' + scenario + ' in ' + region +' from 2010-2100.png'
    plt.savefig(name_of_fig)
    plt.show()

def create_heatmap_std(year, scenario, region, variable_list):

    #create dataframe with the important data
    heat_map_deviations = data_prep_heat_map(year, scenario, region, variable_list)
    #create heat map data frame with the deviations

    for i, mean in heat_map_deviations.mean().items():
        heat_map_deviations.loc[:,i] = heat_map_deviations.loc[:,i] - mean

    #divide by standard deviation

    for n, std in heat_map_deviations.std(axis = 0).items():
        heat_map_deviations.loc[:,n] = heat_map_deviations.loc[:,n] / std

    n_cols = np.arange(len(heat_map_deviations.columns))
    n_rows = np.arange(len(heat_map_deviations.index))


    #plot the heat map


    plt.imshow(heat_map_deviations, cmap='RdYlGn', interpolation='none')
    plt.title('Heatmap (STD) ' + year + ' ' + scenario +' for ' + region)
    plt.colorbar()
    plt.yticks(n_rows, heat_map_deviations.index.values)
    plt.xticks(n_cols, list(heat_map_deviations.columns.values), rotation = 'vertical')
    name_of_fig = saving_location + 'Heatmap of STD per model of' + scenario + ' in ' + year + ' in ' + region +'.png'
    plt.savefig(name_of_fig)
    plt.show()



def create_heatmap_max_one(year, scenario, region, variable_list):

    #create dataframe with the important data

    heat_map_deviations = data_prep_heat_map(year, scenario, region, variable_list)

    #create heat map data frame with the deviations

    for i, mean in heat_map_deviations.mean().items():
        heat_map_deviations.loc[:,i] = heat_map_deviations.loc[:,i] - mean

    #divide by largest absolute value

    for n, maxi in heat_map_deviations.abs().max().iteritems():
        if maxi != 0:
            heat_map_deviations.loc[:,n] = heat_map_deviations.loc[:,n] / maxi


    n_cols = np.arange(len(heat_map_deviations.columns))
    n_rows = np.arange(len(heat_map_deviations.index))


    #plot the heat map
    plt.imshow(heat_map_deviations, cmap='RdYlGn', interpolation='none')
    plt.title('Heatmap (max. 1) ' + year + ' ' + scenario +' for ' + region)
    plt.colorbar()
    plt.yticks(n_rows, heat_map_deviations.index.values)
    plt.xticks(n_cols, list(heat_map_deviations.columns.values), rotation = 'vertical')
    name_of_fig = saving_location +'Heatmap of deviation maximum one of ' + scenario + ' in ' + year + ' in ' + region +'.png'
    plt.savefig(name_of_fig)
    plt.show()


def create_heatmap_percentage(year, scenario, region, variable_list):
    
    #create dataframe with the important data
    heat_map_deviations = data_prep_heat_map(year, scenario, region, variable_list)
    heat_map_deviations = drop_unwanted_models(heat_map_deviations)
    
    #create heat map data frame with the deviations in percentages
    for i, mean in heat_map_deviations.mean().items():
        heat_map_deviations.loc[:,i] = heat_map_deviations.loc[:, i] - mean
        heat_map_deviations.loc[:,i] = heat_map_deviations.loc[:,i] / abs(mean)


    heat_map_deviations = sort_the_df(heat_map_deviations)
    a = heat_map_deviations.max().max()
    b = heat_map_deviations.min().min()
    if abs(b) > a:
        col_bar_set = -b
    else:
        col_bar_set = a
        
    #plot the heat map
    n_cols = np.arange(len(heat_map_deviations.columns))
    n_rows = np.arange(len(heat_map_deviations.index))
    plt.imshow(heat_map_deviations, cmap='RdYlGn', interpolation='none', vmin = -col_bar_set, vmax = col_bar_set)
    a,b = plt.ylim()
    c,d = plt.xlim()
    plt.title('Heatmap ' + year + ' ' + scenario +' for ' + region)
    plt.colorbar()
    plt.yticks(n_rows, heat_map_deviations.index.values)
    plt.xticks(n_cols, list(heat_map_deviations.columns.values), rotation = 'vertical')
    plt.autoscale(False)
    plt.axis((c,d,a,b))
    name_of_fig = saving_location +'Heatmap of deviation in percentage of ' + scenario + ' in ' + year + ' in ' + region + '.png'
    plt.savefig(name_of_fig)
    plt.show()
    

def create_heatmap_baseyear_percentage_relative(year, baseyear, scenario, region, variable_list):
    
    #create dataframe with the important data
    heat_map_deviations = data_prep_heat_map(year, scenario, region, variable_list)
    heat_map_deviations_baseyear = data_prep_heat_map(baseyear, scenario, region, variable_list)
    
    #create heat map data frame with the deviations in percentages

    for i,_ in heat_map_deviations_baseyear.items():
        #subtract baseyear from year
        heat_map_deviations.loc[:,i] = heat_map_deviations.loc[:,i] - heat_map_deviations_baseyear.loc[:,i]
        #divide by baseyear to get relative changes instead of absolute
        heat_map_deviations.loc[:,i] = heat_map_deviations.loc[:,i] / heat_map_deviations_baseyear.loc[:,i]
    
    
    for i, mean in heat_map_deviations.mean().items():
        print(i, ' | ', mean, ' mean of relative change')
        #subtract mean of the changes 
        heat_map_deviations.loc[:,i] = heat_map_deviations.loc[:, i] - mean
        #divide by mean to get the percentages of deviation (absolute mean, to not switch the signs if the mean is negative)
        heat_map_deviations.loc[:,i] = 100 * heat_map_deviations.loc[:,i] / abs(mean)

#plot the heat map
        
    n_cols = np.arange(len(heat_map_deviations.columns))
    n_rows = np.arange(len(heat_map_deviations.index))
    plt.imshow(heat_map_deviations, cmap='RdYlGn', interpolation='none')
    plt.title('Heatmap ' + year + ' ' + scenario +' for ' + region)
    plt.colorbar()
    plt.yticks(n_rows, heat_map_deviations.index.values)
    plt.xticks(n_cols, list(heat_map_deviations.columns.values), rotation = 'vertical')
    name_of_fig = saving_location +'Heatmap in percentage  relative to baseyear ' + baseyear +  ' of ' + scenario + ' in ' + year + ' in ' + region + '.png'
    plt.savefig(name_of_fig)
    plt.show()

def create_heatmap_baseyear_percentage_absolute(year, baseyear, scenario, region, variable_list):
    
    #create dataframe with the important data
    heat_map_deviations = data_prep_heat_map(year, scenario, region, variable_list)
    heat_map_deviations_baseyear = data_prep_heat_map(baseyear, scenario, region, variable_list)
    
    #subtract baseyear from year
    for i,_ in heat_map_deviations_baseyear.items():
        heat_map_deviations.loc[:,i] = heat_map_deviations.loc[:,i] - heat_map_deviations_baseyear.loc[:,i]
        
    #subtract and divide by the mean to get changes in percentages (absolute mean to keep signs in case mean is negative)
    for i, mean in heat_map_deviations.mean().items():
        print(i, ' | ', mean, ' mean of absolute change')
        heat_map_deviations.loc[:,i] = heat_map_deviations.loc[:, i] - mean
        heat_map_deviations.loc[:,i] = 100 * heat_map_deviations.loc[:,i] / abs(mean)
#plot the heat map
        
    n_cols = np.arange(len(heat_map_deviations.columns))
    n_rows = np.arange(len(heat_map_deviations.index))
    plt.imshow(heat_map_deviations, cmap='RdYlGn', interpolation='none')
    plt.title('Heatmap ' + year + ' ' + scenario +' for ' + region)
    plt.colorbar()
    plt.yticks(n_rows, heat_map_deviations.index.values)
    plt.xticks(n_cols, list(heat_map_deviations.columns.values), rotation = 'vertical')
    name_of_fig = saving_location + 'Heatmap in percentage  absolute to baseyear ' + baseyear +  ' of ' + scenario + ' in ' + year + ' in ' + region + '.png'
    plt.savefig(name_of_fig)
    plt.show()
    
    

def create_heatmap_baseyear_std_absolute(year, baseyear, scenario, region, variable_list):
#create dataframe with the important data
    heat_map_deviations = data_prep_heat_map(year, scenario, region, variable_list)
    heat_map_deviations_baseyear = data_prep_heat_map(baseyear, scenario, region, variable_list)


    #subtract baseyear from year
    for i,_ in heat_map_deviations_baseyear.items():
        heat_map_deviations.loc[:,i] = heat_map_deviations.loc[:,i] - heat_map_deviations_baseyear.loc[:,i]
        
    #subtract the mean of the changes
    for i, mean in heat_map_deviations.mean().items():
        heat_map_deviations.loc[:,i] = heat_map_deviations.loc[:, i] - mean
        
    #divide devitations by std
    for n, std in heat_map_deviations.std(axis = 0).items():
        heat_map_deviations.loc[:,n] = heat_map_deviations.loc[:,n] / std
        print(i, ' | ', std, ' standard deviation of absolute change')
    
    
    #plot the heat map
        
    n_cols = np.arange(len(heat_map_deviations.columns))
    n_rows = np.arange(len(heat_map_deviations.index))
    plt.imshow(heat_map_deviations, cmap='RdYlGn', interpolation='none')
    plt.title('Heatmap ' + year + ' ' + scenario +' for ' + region)
    plt.colorbar()
    plt.yticks(n_rows, heat_map_deviations.index.values)
    plt.xticks(n_cols, list(heat_map_deviations.columns.values), rotation = 'vertical')
    name_of_fig = saving_location + 'Heatmap in STD absolute to baseyear ' + baseyear +  ' of ' + scenario + ' in ' + year + ' in ' + region + '.png'
    plt.savefig(name_of_fig)
    plt.show()
    


def create_heatmap_baseyear_std_relative(year, baseyear, scenario, region, variable_list):
    #create dataframe with the important data
    heat_map_deviations = data_prep_heat_map(year, scenario, region, variable_list)
    heat_map_deviations_baseyear = data_prep_heat_map(baseyear, scenario, region, variable_list)

    #drop unwanted models
    heat_map_deviations = drop_unwanted_models(heat_map_deviations)
    heat_map_deviations_baseyear = drop_unwanted_models(heat_map_deviations_baseyear)

    #subtract and divide by baseyear to get relative change
    for i,_ in heat_map_deviations_baseyear.items():
        heat_map_deviations.loc[:,i] = heat_map_deviations.loc[:,i] - heat_map_deviations_baseyear.loc[:,i]
        heat_map_deviations.loc[:,i] = heat_map_deviations.loc[:,i] / heat_map_deviations_baseyear.loc[:,i]
    
    #subtract mean of deviations
    for i, mean in heat_map_deviations.mean().items():
        heat_map_deviations.loc[:,i] = heat_map_deviations.loc[:, i] - mean
      
    #divide by standard deviation
    for n, std in heat_map_deviations.std(axis = 0).items():
        heat_map_deviations.loc[:,n] = heat_map_deviations.loc[:,n] / std
        
    heat_map_deviations = sort_the_df(heat_map_deviations)
    a = heat_map_deviations.max().max()
    b = heat_map_deviations.min().min()
    if abs(b) > a:
        col_bar_set = -b
    else:
        col_bar_set = a


    #plot the heat map
    n_cols = np.arange(len(heat_map_deviations.columns))
    n_rows = np.arange(len(heat_map_deviations.index))
    plt.imshow(heat_map_deviations, cmap='RdYlGn', interpolation='none', vmin = -col_bar_set, vmax = col_bar_set)
    #save full extend of y-axs
    a,b = plt.ylim()
    c,d = plt.xlim()
    
    plt.title('Heatmap ' + year + '  compared relative to ' + baseyear + ' ' + scenario +' for ' + region)
    plt.colorbar()
    
    
    plt.yticks(n_rows, heat_map_deviations.index.values)
    plt.xticks(n_cols, list(heat_map_deviations.columns.values), rotation = 'vertical')
    #adjust y-axis
    plt.autoscale(False)
    plt.axis((c,d,a,b))
    #save figure
    name_of_fig = saving_location + ' Standard Deviation relative to baseyear of ' + region + " in " + year + ' relative to baseyear ' + baseyear + ' of scenario ' + scenario + ' for ' +  str(variable_list[0]) + ' and others.png'
    plt.savefig(name_of_fig.replace('|',''), bbox_inches='tight')
    plt.show()
    
def create_heatmap_baseyear_relative(year, baseyear, scenario, region, variable_list):
    #create dataframe with the important data
    heat_map_deviations = data_prep_heat_map(year, scenario, region, variable_list)
    heat_map_deviations_baseyear = data_prep_heat_map(baseyear, scenario, region, variable_list)

    #drop unwanted models
    heat_map_deviations = drop_unwanted_models(heat_map_deviations)
    heat_map_deviations_baseyear = drop_unwanted_models(heat_map_deviations_baseyear)

    
    #subtract and divide by baseyear to get relative change
    for i,_ in heat_map_deviations_baseyear.items():
#       
        heat_map_deviations.loc[:,i] = heat_map_deviations.loc[:,i] / heat_map_deviations_baseyear.loc[:,i]
    #subtract mean of deviations
    for i, mean in heat_map_deviations.mean().items():
        heat_map_deviations.loc[:,i] = heat_map_deviations.loc[:, i] - mean
      

    heat_map_deviations = sort_the_df(heat_map_deviations)
    a = heat_map_deviations.max().max()
    b = heat_map_deviations.min().min()
    if abs(b) > a:
        col_bar_set = -b
    else:
        col_bar_set = a


    #plot the heat map
    n_cols = np.arange(len(heat_map_deviations.columns))
    n_rows = np.arange(len(heat_map_deviations.index))
    plt.imshow(heat_map_deviations, cmap='RdYlGn', interpolation='none', vmin = -col_bar_set, vmax = col_bar_set)
    #save full extend of y-axs
    a,b = plt.ylim()
    c,d = plt.xlim()
    
    plt.title('Heatmap ' + year + ' compared relative to ' + baseyear + ' ' + scenario +' for ' + region)
    plt.colorbar()
    
    
    plt.yticks(n_rows, heat_map_deviations.index.values)
    plt.xticks(n_cols, list(heat_map_deviations.columns.values), rotation = 'vertical')
    #adjust y-axis
    plt.autoscale(False)
    plt.axis((c,d,a,b))
    #save figure
    name_of_fig = saving_location + ' Standard Deviation relative to baseyear of ' + region + " in " + year + ' relative to baseyear ' + baseyear + ' of scenario ' + scenario + ' for ' +  str(variable_list[0]) + ' and others.png'
    plt.savefig(name_of_fig.replace('|',''), bbox_inches='tight')
    plt.show()
    
    
def create_heatmap_baseyear_absolute(year, baseyear, scenario, region, variable_list):
    #create dataframe with the important data
    heat_map_deviations = data_prep_heat_map(year, scenario, region, variable_list)
    heat_map_deviations_baseyear = data_prep_heat_map(baseyear, scenario, region, variable_list)

    #drop unwanted models
    heat_map_deviations = drop_unwanted_models(heat_map_deviations)
    heat_map_deviations_baseyear = drop_unwanted_models(heat_map_deviations_baseyear)

    
    #subtract and divide by baseyear to get relative change
    for i,_ in heat_map_deviations_baseyear.items():
#       
        heat_map_deviations.loc[:,i] = heat_map_deviations.loc[:,i] - heat_map_deviations_baseyear.loc[:,i]
    print(heat_map_deviations)
    #subtract mean of deviations
    for i, mean in heat_map_deviations.mean().items():
        heat_map_deviations.loc[:,i] = (heat_map_deviations.loc[:, i] - mean) / mean
    print(heat_map_deviations)

    heat_map_deviations = sort_the_df(heat_map_deviations)
    a = heat_map_deviations.max().max()
    b = heat_map_deviations.min().min()
    if abs(b) > a:
        col_bar_set = -b
    else:
        col_bar_set = a


    #plot the heat map
    n_cols = np.arange(len(heat_map_deviations.columns))
    n_rows = np.arange(len(heat_map_deviations.index))
    plt.imshow(heat_map_deviations, cmap='RdYlGn', interpolation='none', vmin = -col_bar_set, vmax = col_bar_set)
    #save full extend of y-axs
    a,b = plt.ylim()
    c,d = plt.xlim()
    
    plt.title('Heatmap ' + year + ' compared absolute to ' + baseyear + ' ' + scenario +' for ' + region)
    plt.colorbar()
    
    
    plt.yticks(n_rows, heat_map_deviations.index.values)
    plt.xticks(n_cols, list(heat_map_deviations.columns.values), rotation = 'vertical')
    #adjust y-axis
    plt.autoscale(False)
    plt.axis((c,d,a,b))
    #save figure
    name_of_fig = saving_location + ' Standard Deviation relative to baseyear of ' + region + " in " + year + ' relative to baseyear ' + baseyear + ' of scenario ' + scenario + ' for ' +  str(variable_list[0]) + ' and others.png'
    plt.savefig(name_of_fig.replace('|',''), bbox_inches='tight')
    plt.show()
    
def create_heatmap_wo_std(scenario, region, variable_list):
    #create dataframe with the important data
    heat_map_final = pd.DataFrame()
    years = ['2010', '2020', '2030', '2040', '2050']
    
    
    for yr in years:
        
        heat_map_deviations = data_prep_heat_map(yr, scenario, region, variable_list)
        
        #drop unwanted models
        heat_map_deviations = drop_unwanted_models(heat_map_deviations)
        #subtract mean of deviations
        for i, mean in heat_map_deviations.mean().items():
            heat_map_deviations.loc[:,i] = heat_map_deviations.loc[:, i] / mean - 1
        heat_map_final = heat_map_final + heat_map_deviations
    heat_map_final = heat_map_final/len(years)
      

    heat_map_deviations = sort_the_df(heat_map_deviations)
    a = heat_map_deviations.max().max()
    b = heat_map_deviations.min().min()
    if abs(b) > a:
        col_bar_set = -b
    else:
        col_bar_set = a


    #plot the heat map
    n_cols = np.arange(len(heat_map_deviations.columns))
    n_rows = np.arange(len(heat_map_deviations.index))
    plt.imshow(heat_map_deviations, cmap='RdYlGn', interpolation='none', vmin = -col_bar_set, vmax = col_bar_set)
    #save full extend of y-axs
    a,b = plt.ylim()
    c,d = plt.xlim()
    
    plt.title('Heatmap   compared relative to ' + scenario +' for ' + region)
    plt.colorbar()
    
    
    plt.yticks(n_rows, heat_map_deviations.index.values)
    plt.xticks(n_cols, list(heat_map_deviations.columns.values), rotation = 'vertical')
    #adjust y-axis
    plt.autoscale(False)
    plt.axis((c,d,a,b))
    #save figure
    name_of_fig = saving_location + ' Standard Deviation relative to baseyear of ' + region  + scenario + ' for ' +  str(variable_list[0]) + ' and others.png'
    plt.savefig(name_of_fig.replace('|',''), bbox_inches='tight')
    plt.show()
    
def fusematrix(name_matrix, new_data, unit):
    name_matrix = name_matrix.set_index(name_matrix.loc[:,'MODEL'])
    name_matrix = name_matrix.drop(['MODEL','SCENARIO', 'REGION', 'VARIABLE', 'UNIT'], axis = 1)
    name_matrix.columns = [unit]
    new_data = pd.concat([new_data, name_matrix], axis = 1)

    return new_data


#creates heat map of deviation of all models on all regions for one variable
def create_heat_map_regions_percentage(year, scenario, variable):
    
    #get relevant data
    region = 'all'
    model = 'all'
    original_values = getyear(variable, region, scenario, model, year)
    original_values = original_values.set_index(original_values.loc[:,'MODEL'])
    original_values = original_values.drop(['VARIABLE', 'MODEL', 'SCENARIO', 'UNIT'], axis = 1)
    
    #prepare data
    #put all the rows of the same model and region into on row by stacking and then unstack them to get usable table
    heat_map_deviations = original_values.copy().reset_index().set_index(['MODEL', 'REGION']).unstack(level=-1)

    #remove another layer of stacking
    heat_map_deviations = heat_map_deviations[year]
    
    #get the percentage deviation of average
    for region_code, average  in heat_map_deviations.mean().iteritems():
        heat_map_deviations.loc[:,region_code] = heat_map_deviations.loc[:,region_code] - average
        heat_map_deviations.loc[:,region_code] = 100 * heat_map_deviations.loc[:,region_code] / abs(average)
      
        
    #create graph
    n_cols = np.arange(len(heat_map_deviations.columns))
    n_rows = np.arange(len(heat_map_deviations.index))
    
    plt.imshow(heat_map_deviations, cmap='RdYlGn', interpolation='none')
    plt.title(year + ' ' + scenario +' for ' + variable)
    plt.colorbar()
    plt.yticks(n_rows, heat_map_deviations.index.values)
    plt.xticks(n_cols, heat_map_deviations.columns.values, rotation = 'vertical')
    name_of_fig = saving_location + 'Deviation in percentages of mean of all regions in ' + year + ' for ' + variable.replace('|', ' ') + '.png'
    plt.savefig(name_of_fig, bbox_inches='tight')
    plt.show()
    


#creates heat map of deviations of all models for one region on different variables
def create_heat_map_comparison_to_baseyear_percentage(year, baseyear, scenario, region, variable_list):

    #get necessariy data
    heat_map_deviations = data_prep_heat_map(year, scenario, region, variable_list)
    heat_map_baseyear = data_prep_heat_map(baseyear, scenario, region, variable_list)
    #subtract base year
    heat_map_deviations = heat_map_deviations - heat_map_baseyear
    #get mean/percentage values
    for i, mean in heat_map_deviations.mean().items():
        
        heat_map_deviations.loc[:,i] = heat_map_deviations.loc[:, i] - mean
        heat_map_deviations.loc[:,i] = 100 * heat_map_deviations.loc[:,i] / abs(mean)


    #create heat map data frame with the deviations
    n_cols = np.arange(len(heat_map_deviations.columns))
    n_rows = np.arange(len(heat_map_deviations.index))
    plt.imshow(heat_map_deviations, cmap='RdYlGn', interpolation='none')
    plt.title(year + ' ' + scenario +' for ' + region)
    plt.colorbar()
    plt.yticks(n_rows, heat_map_deviations.index.values)
    plt.xticks(n_cols, heat_map_deviations.columns.values, rotation = 'vertical')
    name_of_fig = saving_location + 'Deviation in percentages of mean in ' + year + ' compared to baseyear ' + baseyear + ' in scenario ' + scenario + '.png'
    plt.savefig(name_of_fig.replace('|', ' '), bbox_inches='tight')
    plt.show()


#shows for all models and selected region the deviation in percentage compared to population
def create_heat_map_regions_pop_percentage(year, scenario, variable, region_list):

    #prepare table
    model = 'all'
    original_values = pd.DataFrame()

    #get the values for the year and variable
    for i in region_list:
        new_data = getyear(variable, i, scenario, model, year)
        new_data = new_data.set_index(new_data.loc[:,'MODEL'])
        new_data = new_data.drop(['VARIABLE', 'MODEL', 'SCENARIO', 'UNIT'], axis = 1)
        original_values = original_values.append(new_data)
    original_values = original_values.rename(columns={year:variable})

    #get the percentages of the deviation for variable
    original_values = original_values.reset_index().set_index(['REGION','MODEL']).unstack(level=1).T
    original_values = original_values.loc[variable,:]
    for n, mean in original_values.mean().iteritems():
        original_values.loc[:,n] = original_values.loc[:,n] - mean
        original_values.loc[:,n] = 100 * original_values.loc[:,n] / abs(mean)



    #get the population data for that year
    original_values_pop = pd.DataFrame()
    for i in region_list:
        new_data = getyear('Population', i, scenario, model, year)
        new_data = new_data.set_index(new_data.loc[:,'MODEL'])
        new_data = new_data.drop(['VARIABLE', 'MODEL', 'SCENARIO', 'UNIT'], axis = 1)
        original_values_pop= original_values_pop.append(new_data)

####################################################################################################################
    #The order is correct but will it always be that case?

    #get percentages ofthe deviations for population
    original_values_pop = original_values_pop.reset_index().set_index(['REGION','MODEL']).unstack(level=1).T
    original_values_pop = original_values_pop.loc[year,:]
    for n, mean in original_values_pop.mean().iteritems():
        original_values_pop.loc[:,n] = original_values_pop.loc[:,n] - mean
        original_values_pop.loc[:,n] = 100 * original_values_pop.loc[:,n] / abs(mean)





    #fusing the two df's to one to be able to plot them
    heat_map_deviations = original_values.copy()

    n = 1
    for i,k in original_values_pop.iteritems():
        heat_map_deviations.insert(n,i + ' Population', k)
        n = n+2





    #plotting the df
    n_cols = np.arange(len(heat_map_deviations.columns))
    n_rows = np.arange(len(heat_map_deviations.index))
    plt.imshow(heat_map_deviations, cmap='RdYlGn', interpolation='none')
    plt.title(year + ' ' + scenario + ' ' +variable)
    plt.colorbar()
    plt.yticks(n_rows, heat_map_deviations.index.values)
    plt.xticks(n_cols, heat_map_deviations.columns.values, rotation = 'vertical')
    name_of_fig = saving_location + 'Deviation in percentages of mean in ' + year + ' for ' + variable.replace('|', ' ') + ' for scenario ' + scenario + '.png'
    plt.savefig(name_of_fig, bbox_inches='tight')
    plt.show()


#creates to graphs of population and a variable for all models and specific regions
def create_heat_map_regions_pop_percentage_two_graphs(year, scenario, variable, region_list):

    #prepare table
    model = 'all'
    original_values = pd.DataFrame()

    #get data of variable for the regions
    for i in region_list:
        new_data = getyear(variable, i, scenario, model, year)
        new_data = new_data.set_index(new_data.loc[:,'MODEL'])
        new_data = new_data.drop(['VARIABLE', 'MODEL', 'SCENARIO', 'UNIT'], axis = 1)
        original_values = original_values.append(new_data)
    original_values = original_values.rename(columns={year:variable})

    #prepare table in a proper way for a heat map
    original_values = original_values.reset_index().set_index(['REGION','MODEL']).unstack(level=1).T
    original_values = original_values.loc[variable,:]
    
    #get deviations in percentages
    for n, mean in original_values.mean().iteritems():
        original_values.loc[:,n] = original_values.loc[:,n] - mean
        original_values.loc[:,n] = 100 * original_values.loc[:,n] / abs(mean)



    #get data for population
    original_values_pop = pd.DataFrame()
    for i in region_list:
        new_data = getyear('Population', i, scenario, model, year)
        new_data = new_data.set_index(new_data.loc[:,'MODEL'])
        new_data = new_data.drop(['VARIABLE', 'MODEL', 'SCENARIO', 'UNIT'], axis = 1)
        original_values_pop= original_values_pop.append(new_data)

    #prepare table in proper way for heat map
    original_values_pop = original_values_pop.reset_index().set_index(['REGION','MODEL']).unstack(level=1).T
    original_values_pop = original_values_pop.loc[year,:]
    
    #get deviations in percentages 
    for n, mean in original_values_pop.mean().iteritems():
        original_values_pop.loc[:,n] = original_values_pop.loc[:,n] - mean
        original_values_pop.loc[:,n] = 100 * original_values_pop.loc[:,n] / abs(mean)



    


    #copy data
    heat_map_deviations = original_values.copy()
    heat_map_deviations_pop = original_values_pop.copy()


    #plot variable
    n_cols = np.arange(len(heat_map_deviations.columns))
    n_rows = np.arange(len(heat_map_deviations.index))
    plt.imshow(heat_map_deviations, cmap='RdYlGn', interpolation='none')
    plt.title(year + ' ' + scenario + ' ' +variable)
    plt.colorbar()
    plt.yticks(n_rows, heat_map_deviations.index.values)
    plt.xticks(n_cols, heat_map_deviations.columns.values, rotation = 'vertical')
    name_of_fig = saving_location + 'Regional deviation (percentage) of average of ' + variable.replace('|', ' ') + " in " + year + '.png'
    plt.savefig(name_of_fig, bbox_inches='tight')
    plt.show()

    #plot population
    n_cols = np.arange(len(heat_map_deviations_pop.columns))
    n_rows = np.arange(len(heat_map_deviations_pop.index))
    plt.imshow(heat_map_deviations_pop, cmap='RdYlGn', interpolation='none')
    plt.title(year + ' ' + scenario + ' Population')
    plt.colorbar()
    plt.yticks(n_rows, heat_map_deviations_pop.index.values)
    plt.xticks(n_cols, heat_map_deviations_pop.columns.values, rotation = 'vertical')
    name_of_fig = saving_location + 'Regional deviation (percentage) of average of population in ' + year + '.png'
    plt.savefig(name_of_fig, bbox_inches='tight')
    plt.show()


#create heat map  compared to baseyear of all models, different region and a selected variable
def create_heat_map_regions_pop_percentage_to_baseyear(year, baseyear, scenario, variable, region_list):

    #prepare table
    model = 'all'
    original_values = pd.DataFrame()

    #get data for variable
    for i in region_list:
        new_data = getyear(variable, i, scenario, model, year)
        new_data = new_data.set_index(new_data.loc[:,'MODEL'])
        new_data = new_data.drop(['VARIABLE', 'MODEL', 'SCENARIO', 'UNIT'], axis = 1)
        original_values = original_values.append(new_data)
    original_values = original_values.rename(columns={year:variable})


    #get data for baseyear
    original_values_baseyear = pd.DataFrame()
    for i in region_list:
        new_data1 = getyear(variable, i, scenario, model, baseyear)
        new_data1 = new_data1.set_index(new_data1.loc[:,'MODEL'])
        new_data1 = new_data1.drop(['VARIABLE', 'MODEL', 'SCENARIO', 'UNIT'], axis = 1)
        original_values_baseyear = original_values_baseyear.append(new_data1)
    original_values_baseyear = original_values_baseyear.rename(columns={baseyear:variable})

    #subtract baseyear from year 
    original_values[variable] = original_values[variable] - original_values_baseyear[variable]


    #prepare df to be readable for the graph
    original_values = original_values.reset_index().set_index(['REGION','MODEL']).unstack(level=1).T
    original_values = original_values.loc[variable,:]
    

    #create percentages of deviation for variable
    for n, mean in original_values.mean().iteritems():
        original_values.loc[:,n] = original_values.loc[:,n] - mean
        original_values.loc[:,n] = 100 * original_values.loc[:,n] / abs(mean)
    original_values_baseyear = original_values_baseyear.rename(columns={year:variable})



    #same procedure as above but for the baseyear
    original_values_pop = pd.DataFrame()
    for i in region_list:
        new_data = getyear('Population', i, scenario, model, year)
        new_data = new_data.set_index(new_data.loc[:,'MODEL'])
        new_data = new_data.drop(['VARIABLE', 'MODEL', 'SCENARIO', 'UNIT'], axis = 1)
        original_values_pop= original_values_pop.append(new_data)


    original_values_pop_baseyear = pd.DataFrame()
    for i in region_list:
        new_data1 = getyear('Population', i, scenario, model, baseyear)
        new_data1 = new_data1.set_index(new_data1.loc[:,'MODEL'])
        new_data1 = new_data1.drop(['VARIABLE', 'MODEL', 'SCENARIO', 'UNIT'], axis = 1)
        original_values_pop_baseyear = original_values_pop_baseyear.append(new_data1)

    original_values_pop['Population'] = original_values_pop[year] - original_values_pop_baseyear[baseyear]
    del original_values_pop[year]
    original_values_pop = original_values_pop.rename(columns={'Population':year})



    original_values_pop = original_values_pop.reset_index().set_index(['REGION','MODEL']).unstack(level=1).T
    original_values_pop = original_values_pop.loc[year,:]
    for n, mean in original_values_pop.mean().iteritems():
        original_values_pop.loc[:,n] = original_values_pop.loc[:,n] - mean
        original_values_pop.loc[:,n] = 100 * original_values_pop.loc[:,n] / abs(mean)



    #fuse two matrices of variable and population
    heat_map_deviations = original_values.copy()

    n = 1
    for i,k in original_values_pop.iteritems():
        heat_map_deviations.insert(n,i + ' Population', k)
        n = n+2




    #plot df 
    n_cols = np.arange(len(heat_map_deviations.columns))
    n_rows = np.arange(len(heat_map_deviations.index))
    plt.imshow(heat_map_deviations, cmap='RdYlGn', interpolation='none')
    plt.title(year + ' ' + scenario + ' ' +variable)
    plt.colorbar()
    plt.yticks(n_rows, heat_map_deviations.index.values)
    plt.xticks(n_cols, heat_map_deviations.columns.values, rotation = 'vertical')
    name_of_fig = saving_location + 'Deviation in percentages of mean in ' + year + ' compared to baseyear ' + baseyear + ' for ' + variable.replace('|', ' ') + ' for scenario ' + scenario + '.png'
    plt.savefig(name_of_fig, bbox_inches='tight')
    plt.show()



#create heat map  compared to baseyear of all models, different region and a selected variable
#the same procedure as function: create_heat_map_regions_pop_percentage_to_baseyear, but without the fusion of both df's
def create_heat_map_regions_pop_percentage_to_baseyear_two_graphs(year, baseyear, scenario, variable, region_list):

    #prepare table
    model = 'all'
    original_values = pd.DataFrame()
    
    #get data
    for i in region_list:
        new_data = getyear(variable, i, scenario, model, year)
        new_data = new_data.set_index(new_data.loc[:,'MODEL'])
        new_data = new_data.drop(['VARIABLE', 'MODEL', 'SCENARIO', 'UNIT'], axis = 1)
        original_values = original_values.append(new_data)
    original_values = original_values.rename(columns={year:variable})

    original_values_baseyear = pd.DataFrame()
    for i in region_list:
        new_data1 = getyear(variable, i, scenario, model, baseyear)
        new_data1 = new_data1.set_index(new_data1.loc[:,'MODEL'])
        new_data1 = new_data1.drop(['VARIABLE', 'MODEL', 'SCENARIO', 'UNIT'], axis = 1)
        original_values_baseyear = original_values_baseyear.append(new_data1)
    original_values_baseyear = original_values_baseyear.rename(columns={baseyear:variable})


    original_values[variable] = original_values[variable] - original_values_baseyear[variable]


    original_values = original_values.reset_index().set_index(['REGION','MODEL']).unstack(level=1).T
    original_values = original_values.loc[variable,:]
    for n, mean in original_values.mean().iteritems():
        original_values.loc[:,n] = original_values.loc[:,n] - mean
        original_values.loc[:,n] = 100 * original_values.loc[:,n] / abs(mean)





    original_values_pop = pd.DataFrame()
    for i in region_list:
        new_data = getyear('Population', i, scenario, model, year)
        new_data = new_data.set_index(new_data.loc[:,'MODEL'])
        new_data = new_data.drop(['VARIABLE', 'MODEL', 'SCENARIO', 'UNIT'], axis = 1)
        original_values_pop= original_values_pop.append(new_data)

    original_values_pop_baseyear = pd.DataFrame()
    for i in region_list:
        new_data1 = getyear('Population', i, scenario, model, baseyear)
        new_data1 = new_data1.set_index(new_data1.loc[:,'MODEL'])
        new_data1 = new_data1.drop(['VARIABLE', 'MODEL', 'SCENARIO', 'UNIT'], axis = 1)
        original_values_pop_baseyear = original_values_pop_baseyear.append(new_data1)

    original_values_pop['Population'] = original_values_pop[year] - original_values_pop_baseyear[baseyear]
    del original_values_pop[year]
    original_values_pop = original_values_pop.rename(columns={'Population':year})


    original_values_pop = original_values_pop.reset_index().set_index(['REGION','MODEL']).unstack(level=1).T
    original_values_pop = original_values_pop.loc[year,:]
    for n, mean in original_values_pop.mean().iteritems():
        original_values_pop.loc[:,n] = original_values_pop.loc[:,n] - mean
        original_values_pop.loc[:,n] = 100 * original_values_pop.loc[:,n] / abs(mean)


    heat_map_deviations = original_values.copy()
    heat_map_deviations_pop = original_values_pop.copy()



    #plot the two df's in two plots
    n_cols = np.arange(len(heat_map_deviations.columns))
    n_rows = np.arange(len(heat_map_deviations.index))
    plt.imshow(heat_map_deviations, cmap='RdYlGn', interpolation='none')
    plt.title(year + ' ' + scenario + ' ' +variable)
    plt.colorbar()
    plt.yticks(n_rows, heat_map_deviations.index.values)
    plt.xticks(n_cols, heat_map_deviations.columns.values, rotation = 'vertical')
    name_of_fig = saving_location + 'Deviation in percentages of mean in ' + year + ' compared to baseyear ' + baseyear + ' for ' + variable.replace('|', ' ') + ' for scenario ' + scenario + '.png'
    plt.savefig(name_of_fig, bbox_inches='tight')
    plt.show()

    n_cols = np.arange(len(heat_map_deviations_pop.columns))
    n_rows = np.arange(len(heat_map_deviations_pop.index))
    plt.imshow(heat_map_deviations_pop, cmap='RdYlGn', interpolation='none')
    plt.title(year + ' ' + scenario + ' Population')
    plt.colorbar()
    plt.yticks(n_rows, heat_map_deviations_pop.index.values)
    plt.xticks(n_cols, heat_map_deviations_pop.columns.values, rotation = 'vertical')
    name_of_fig = saving_location + 'Deviation in percentages of mean in ' + year + ' compared to baseyear ' + baseyear + ' for population for scenario ' + scenario + '.png'
    plt.savefig(name_of_fig, bbox_inches='tight')
    plt.show()



#creates heat map of variables and regions on their std/average
def create_heat_map_std(year, scenario, regions, variable_list):

    #create df
    heat_map_std = pd.DataFrame()
    
    #retrieve data for variables and regions
    for region in regions:

        #get list of data for the region
        heat_map_deviations = data_prep_heat_map(year, scenario, region, variable_list)
        #delete unwanted models
        heat_map_deviations = drop_unwanted_models(heat_map_deviations)
        #insert the std/average value into the right region column of the heat map
        heat_map_std[region] = heat_map_deviations.std() / heat_map_deviations.mean().abs()




    #create heat map data frame with the deviations
    n_cols = np.arange(len(heat_map_std.columns))
    n_rows = np.arange(len(heat_map_std.index))

    plt.imshow(heat_map_std, cmap= 'OrRd', interpolation='none')
    a,b = plt.ylim()
    c,d = plt.xlim()
    
    plt.title(year + ' ' + scenario +' STD ')
    plt.colorbar()
    plt.yticks(n_rows, heat_map_std.index.values)
    plt.xticks(n_cols, heat_map_std.columns.values, rotation = 'vertical')
    plt.autoscale(False)
    plt.axis((c,d,a,b))
    name_of_fig = saving_location + 'Standard Deviation of regions and variables in ' + year + '.png'
    plt.savefig(name_of_fig, bbox_inches='tight')
    plt.show()
    

#creates heat map of variables and regions on their std/average for all years
def create_heat_map_std_all_years(scenario, regions, variable_list):

    #create df
    heat_map_std = pd.DataFrame()
    
    years = ['2010','2020','2030','2040','2050','2060','2070']#,'2080','2090','2100',]
    #retrieve data for variables and regions
    for yr in years:
        for region in regions:
            #get list of data for the region
            heat_map_deviations = data_prep_heat_map(yr, scenario, region, variable_list)
            #insert the std/average value into the right region column of the heat map
            heat_map_std[region] = heat_map_deviations.std() / heat_map_deviations.mean().abs()
        print(yr)
        
    #adjust for number of years
    heat_map_std = heat_map_std / len(years)


    #create heat map data frame with the deviations
    n_cols = np.arange(len(heat_map_std.columns))
    n_rows = np.arange(len(heat_map_std.index))

    plt.imshow(heat_map_std, cmap= 'OrRd', interpolation='none')
    plt.title('all years' + scenario +' STD ')
    plt.colorbar()
    plt.yticks(n_rows, heat_map_std.index.values)
    plt.xticks(n_cols, heat_map_std.columns.values, rotation = 'vertical')
    name_of_fig = saving_location + 'Standard Deviation of regions and variables from ' + years[0] + ' till ' + years[-1] +'.png'
    plt.savefig(name_of_fig, bbox_inches='tight')
    plt.show()


#creates heat map of variables and regions on their std/average compared to baseyear
def create_heat_map_std_to_baseyear(year, baseyear, scenario, regions, variable_list):

    #create df
    heat_map_std = pd.DataFrame()
    
    #retrieve data for variables, vbaseyear and region
    for region in regions:

        #get list of data for the region
        heat_map_deviations_year = data_prep_heat_map(year, scenario, region, variable_list)
        #get list of data for the region and baseyear
        heat_map_deviations_baseyear = data_prep_heat_map(baseyear, scenario, region, variable_list)
        #subtract data of year by baseyear
        
        heat_map_deviations = (heat_map_deviations_year - heat_map_deviations_baseyear)/heat_map_deviations_baseyear.abs()
        if region == 'EU':
            print(heat_map_deviations_baseyear, heat_map_deviations_year, heat_map_deviations,heat_map_deviations.std(), heat_map_deviations.mean())
        
        #insert the std/average value into the right region column of the heat map
        heat_map_std[region] = heat_map_deviations.std() / heat_map_deviations.mean().abs()

        


    #create heat map data frame with the deviations
    n_cols = np.arange(len(heat_map_std.columns))
    n_rows = np.arange(len(heat_map_std.index))
    plt.imshow(heat_map_std, cmap= 'OrRd', interpolation='none')
    plt.title(year + ' ' + scenario +' STD ')
    plt.colorbar()
    plt.yticks(n_rows, heat_map_std.index.values)
    plt.xticks(n_cols, heat_map_std.columns.values, rotation = 'vertical')
    name_of_fig = saving_location + 'Standard Deviation of regions and variables in ' + year + '.png'
    plt.savefig(name_of_fig, bbox_inches='tight')
    plt.show()
    
 

def create_heat_map_std_to_baseyear_relative2(year, baseyear, scenario, regions, variable_list):

    #create df
    heat_map_std = pd.DataFrame()
    
    #retrieve data for variables, vbaseyear and region
    for region in regions:

        #get list of data for the region
        heat_map_deviations_year = data_prep_heat_map(year, scenario, region, variable_list)
        #get list of data for the region and baseyear
        heat_map_deviations_baseyear = data_prep_heat_map(baseyear, scenario, region, variable_list)
        #subtract data of year by baseyear
        
        heat_map_deviations = (heat_map_deviations_year - heat_map_deviations_baseyear)/heat_map_deviations_baseyear.abs()
        #insert the std/average value into the right region column of the heat map
        heat_map_std[region] = heat_map_deviations.std() / heat_map_deviations.mean().abs()

        


    #create heat map data frame with the deviations
    n_cols = np.arange(len(heat_map_std.columns))
    n_rows = np.arange(len(heat_map_std.index))
    plt.imshow(heat_map_std, cmap= 'OrRd', interpolation='none')
    plt.title(year + ' ' + scenario +' STD ')
    plt.colorbar()
    plt.yticks(n_rows, heat_map_std.index.values)
    plt.xticks(n_cols, heat_map_std.columns.values, rotation = 'vertical')
    name_of_fig = saving_location + 'Standard Deviation of regions and variables in ' + year + '.png'
    plt.savefig(name_of_fig, bbox_inches='tight')
    plt.show()


def create_heat_map_std_scenarios(year, scenario_list, region, variable_list):

    #create df
    heat_map_std = pd.DataFrame()
    
    #retrieve data for variables and regions
    for scenario in scenario_list:

        #get list of data for the region
        heat_map_deviations = data_prep_heat_map(year, scenario, region, variable_list)
        #delete unwanted models
        heat_map_deviations = drop_unwanted_models(heat_map_deviations)
        #insert the std/average value into the right region column of the heat map
        heat_map_std[scenario] = heat_map_deviations.std() / heat_map_deviations.mean().abs()




    #create heat map data frame with the deviations
    n_cols = np.arange(len(heat_map_std.columns))
    n_rows = np.arange(len(heat_map_std.index))

    plt.imshow(heat_map_std, cmap= 'OrRd', interpolation='none')
    plt.title(year + ' ' + scenario +' STD ')
    plt.colorbar()
    plt.yticks(n_rows, heat_map_std.index.values)
    plt.xticks(n_cols, heat_map_std.columns.values, rotation = 'vertical')
    name_of_fig = saving_location + 'Standard Deviation of scenarios and variables in ' + year + '.png'
    plt.savefig(name_of_fig, bbox_inches='tight')
    plt.show()




def stacked_graph(year, variable_list, scenario, region):
    
    
 #get list of data for the region
        heat_map_deviations_year = data_prep_heat_map(year, scenario, region, variable_list)
        #drop the unwanted models
        heat_map_deviations_year = drop_unwanted_models(heat_map_deviations_year)
        
        
            
        heat_map_deviations_year.plot(kind='bar', stacked = True)
        plt.xticks(rotation=90)
        y_label = table_1.loc[table_1['VARIABLE'] == variable_list[0], 'UNIT']
        y_label = y_label.iloc[0]
        plt.ylabel(y_label)
        plt.xlabel('') # do not show automatic xlabel
        name_of_fig = saving_location + 'stacked bar graph '+ variable_list[0] + scenario + year + '.png'
        plt.savefig(name_of_fig.replace('|',''), bbox_inches='tight')
        plt.show()



def sort_the_df(df):
    df['Sum'] = df.sum(axis = 1)   
    df = df.sort_values(by = 'Sum')
    df = df.drop('Sum', axis = 1)
    return df


#updates sceanrios so that national and global models have the same sceanrio names
def update_scenarios():

    #loops through the scame_scenario dataframe
    for i in range(len(same_scenarios)):
        for k in range(1, len(same_scenarios.columns)):
            
            # deletes multiple cell values
            for n in range(1, len(same_scenarios.columns)):
                if (same_scenarios.iloc[i,k] == same_scenarios.iloc[i,n]) & (k != n):
                    same_scenarios.iloc[i,k] = np.nan
            print(i,k, print(same_scenarios.iloc[i,k]))
            #replace cell values
            table_1.loc[table_1['SCENARIO'].str[:len(str(same_scenarios.iloc[i,k]))] == str(same_scenarios.iloc[i,k]), 'SCENARIO'] = table_1.loc[table_1['SCENARIO'].str[:len(str(same_scenarios.iloc[i,k]))] == str(same_scenarios.iloc[i,k]), 'SCENARIO'].str.replace(str(same_scenarios.iloc[i,k]),(same_scenarios.iloc[i,0]))
            

#updates all model versions to the latest by replacing the number of the version by 'X'
def update_models():


    #copy Scenario names to new column so the data does not get lost
    table_1['Scenarios original version name'] = table_1['SCENARIO']


    #getting all models 
    list_models = table_1['MODEL'].unique()
    for modelname in list_models:
        
        
        #compiles list of all scenario names
        unique_scenario_names = table_1.loc[(table_1['MODEL'] == modelname), 'SCENARIO'].unique()
        
        #looks for the largest scenario name (latest version) of every scenario
        for scenario_name in np.unique([re.sub('_V[X0-9]','', name) for name in unique_scenario_names]):
            if table_1.loc[table_1['MODEL'] == modelname].empty == False:
            #check if dataframe is not empty
                max_val_list = list(filter(re.compile(str(scenario_name) + '_V.').match, unique_scenario_names))
                if max_val_list:
                    max_val = max(max_val_list)
                    #replaces the latest scenario version with an 'X' instead of a number
                    table_1.loc[(table_1['MODEL'] == modelname) & (table_1['SCENARIO'] == max_val), 'SCENARIO'] = table_1['SCENARIO'].apply(lambda x: '{}{}'.format(x[:-1], 'X'))
       
#drops models that should not be in the df             
def drop_unwanted_models(df):
    
    if 'MODEL' in df:
        #loop over model list and drop of df
        for models in model_list_to_drop:
            df = df.drop(df.loc[df["MODEL"] == models].index)
    else:
        for models in model_list_to_drop:
            if models in df.index:
                df = df.drop(models)
    return df

def del_old_models(df):
    df = df.loc[df['SCENARIO'].str[-2:] == 'VX']
    return df

def subtract_var_2_from_var_1(df, var_1,var_2,new_var_name, new_var_unit):
    
    
        
    #look which ones have primary energy and primary energy fossil values
    df1 = df.loc[df['VARIABLE'] == var_1]
    df2 = df.loc[df['VARIABLE'] == var_2]
    df1 = df1.set_index(['MODEL', 'SCENARIO', 'REGION'])
    df2 = df2.set_index(['MODEL', 'SCENARIO', 'REGION'])
    
    df3 = df1.loc[:,'1990':'2110'] - df2.loc[:,'1990':'2110']
    df3 = df3.reset_index()
    df3['VARIABLE'] = new_var_name
    df3['UNIT'] = new_var_unit
    df3.dropna(thresh = 6, inplace = True)
    df = df.append(df3)
        
    return df


def divide_var_2_by_var_1(df, var_1, var_2, new_var_name, new_var_unit):
    
    #get the variables out
    df1 = df.loc[df['VARIABLE'] == var_1]
    df2 = df.loc[df['VARIABLE'] == var_2]
    #stack them to easier divide them
    df1 = df1.set_index(['MODEL', 'SCENARIO','REGION'])
    df2 = df2.set_index(['MODEL', 'SCENARIO','REGION'])
    
    #divide
    df3 = df2.loc[:,'1990':'2110'] / df1.loc[:,'1990':'2110']
    df3 = df3.reset_index()
    df3['VARIABLE'] = new_var_name
    df3['UNIT'] = new_var_unit
    df3.dropna(thresh = 6, inplace = True)
    df = df.append(df3)
    
    return df


def give_output_data(output_location, name_csv, scenario_list, variable_list, region):
    
    df = pd.DataFrame()
    for scenario in scenario_list:
        for variable in variable_list:
            
                out_df = getrow(variable,region,scenario,'all')
                df = df.append(out_df)
    
    df = df.reset_index()            
    df = df.drop(['Scenarios original version name', 'index'],axis=1)
    
    #rearrange df
    df2 = df.loc[:,'MODEL':'VARIABLE']
    df1 = df.loc[:,'1990':'2110']
    df = df2.join(df1)
    
    
#    df = df[df.columns[::-1]]
    save_spot = output_location + name_csv + '.csv'
    df.to_csv(save_spot, sep=",")

#give_output_data('C:/Users/chris/Desktop/School/Internships/PBL/Outputs/','Data India', ['NPi2020_1000_VX', 'NPi2020_400_VX'], ['Emissions|CO2', 'Final Energy', 'Primary Energy', 'Primary Energy|Renewables', 'Primary Energy|Coal Share', 'Primary Energy|Gas Share','Primary Energy|Oil Share', 'Primary Energy|Renewable Share', 'Secondary Energy|Electricity|Share Renewables' ], 'IND')

####################################################################################################################
#Data preparation
####################################################################################################################

#importing the needed libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import numpy as np
import re
import ctypes
#from tqdm import tqdm


#
table_1 = pd.read_csv("C:/Users/chris/Desktop/School/Internships/PBL/Inputs/cdlinks_compare_20190519-203202.csv", sep=",")
same_scenarios = pd.read_csv('C:/Users/chris/Desktop/School/Internships/PBL/Inputs/Same Scenarios.csv', sep = ',')

update_scenarios()
update_models()

table_1 = del_old_models(table_1)
table_1 = subtract_var_2_from_var_1(table_1, 'Primary Energy', 'Primary Energy|Fossil', 'Primary Energy|Non-Fossil', 'EJ/yr')
table_1 = divide_var_2_by_var_1(table_1,'Primary Energy','Primary Energy|Coal', 'Primary Energy|Coal Share', '')
table_1 = divide_var_2_by_var_1(table_1,'Primary Energy','Primary Energy|Oil', 'Primary Energy|Oil Share', '')
table_1 = divide_var_2_by_var_1(table_1,'Primary Energy','Primary Energy|Gas', 'Primary Energy|Gas Share', '')
table_1 = subtract_var_2_from_var_1(table_1,'Primary Energy|Non-Fossil','Primary Energy|Nuclear', 'Primary Energy|Renewables', 'EJ/yr')
table_1 = divide_var_2_by_var_1(table_1,'Primary Energy','Primary Energy|Renewables', 'Primary Energy|Renewable Share', '')

table_1 = subtract_var_2_from_var_1(table_1,'Secondary Energy|Electricity','Secondary Energy|Electricity|Fossil', 'Secondary Energy|Electricity|Non-Fossil', 'EJ/yr')
table_1 = subtract_var_2_from_var_1(table_1,'Secondary Energy|Electricity|Non-Fossil','Secondary Energy|Electricity|Nuclear', 'Secondary Energy|Electricity|Renewable', 'EJ/yr')
table_1 = divide_var_2_by_var_1(table_1,'Secondary Energy|Electricity','Secondary Energy|Electricity|Renewable', 'Secondary Energy|Electricity|Share Renewables', '')


####################################################################################################################
#Visualisation
####################################################################################################################



variables_to_compare = ['GDP|PPP', 'Population', 'Emissions|CO2', 'Primary Energy', 'Final Energy']
variables_to_compare_long = variables_to_compare + ['Final Energy|Electricity', 'Final Energy|Industry', 'Final Energy|Transportation', 'Primary Energy|Fossil', 'Primary Energy|Non-Fossil', 'Primary Energy|Coal', 'Primary Energy|Gas', 'Primary Energy|Oil']
regions = ['World','CHN','USA', 'EU', 'RUS', 'JPN','IND']
model_list_to_drop = ['AIM/CGE', 'MESSAGEix-GLOBIOM_1.0', 'GLOBIOM 1.0']
saving_location = 'C:/Users/chris/Desktop/School/Internships/PBL/Outputs/Graphs/'

sequence_colors = ['RdYlGn']
colors_PBL = ['#00AEEF', '#808D1D', '#B6036C', '#FAAD1E', '#3F1464', '#7CCFF2', '#F198C1', '#42B649', '#EE2A23', '#004019', '#F47321', '#511607', '#BA8912', '#78CBBF', '#FFF229', '#0071BB']



create_line_graph_2050('Primary Energy|Non-Fossil', 'IND','NPi2020_1000_VX' ,'all')
#create_line_graph_explicit_2010_2100('Final Energy', 'CHN','NPi2020_1000_VX' ,'all') 
#create_heatmap_std('2020', 'NPi2020_1000_VX', 'World', variables_to_compare)
#create_heatmap_max_one('2080', 'NPi2020_1000_VX', 'World', variables_to_compare)
#create_heatmap_percentage('2050', 'NPi2020_1000_VX', 'EU', variables_to_compare)
#create_heat_map_comparison_to_baseyear_percentage('2050', '2020', 'NPi2020_1000_VX', 'World', variables_to_compare)
#create_heat_map_regions_pop_percentage('2050', 'NPi2020_1000_VX', 'Emissions|CO2', regions)
#create_heat_map_regions_pop_percentage_to_baseyear('2050', '2020', 'NPi2020_1000_VX', 'Emissions|CO2', regions)
#create_heat_map_regions_pop_percentage_to_baseyear_two_graphs('2050', '2020', 'NPi2020_1600_VX', 'Emissions|CO2', regions)
#
#create_heatmap_baseyear_percentage_relative('2050', '2020', 'NPi2020_1000_VX', 'IND', variables_to_compare)
#create_heatmap_baseyear_percentage_absolute('2050', '2020', 'NPi2020_1000_V2', 'World', variables_to_compare) 
#create_heatmap_baseyear_std_absolute('2050', '2020', 'NPi2020_1000_VX', 'IND', variables_to_compare)            
#create_heat_map_std_to_baseyear('2050', '2020', 'NPi2020_1000_VX', regions, variables_to_compare)
#create_heat_map_std_all_years('NPi2020_1000_VX', regions, variables_to_compare)
#create_heatmap_baseyear_std_relative('2050', '2020','NPi2020_1000_VX', 'IND', variables_to_compare)
#create_heatmap_wo_std('INDC2030i_1000_VX', 'EU', ['Primary Energy|Coal'])
#stacked_graph('2050', [ 'Final Energy|Industry', 'Final Energy|Transportation', 'Final Energy|Electricity'], 'NPi2020_1000_VX', 'IND')
#create_heat_map_std_scenarios('2050', ['NPi2020_1000_VX','NPi2020_400_VX', 'INDC2030i_1000_VX', 'INDC2030i_400_VX'], 'IND', variables_to_compare)




#create_heat_map_regions_percentage('2020', 'NPi2020_1000_VX', 'Population')
#create_heatmap_baseyear_relative('2060', '2010','NPi2020_1000_VX', 'EU', variables_to_compare)
#create_heat_map_std('2050', 'NPi2020_1000_VX', regions, variables_to_compare_long)
#create_heat_map_regions_pop_percentage_two_graphs('2050', 'NPi2020_1000_VX', 'Emissions|CO2', regions)


#create_heatmap_baseyear_absolute('2050', '2020','INDC2030i_1000_VX', 'EU', variables_to_compare)



####################################################################################################################
#scripts to automate variable output
####################################################################################################################
#out_regions = ['World','USA','EU','CHN','IND','JPN','RUS']
#out_scenarios = ['NPi2020_1000_VX']#,'NPi_VX','NoPolicy_VX']
#variables_to_compare2 = pd.read_csv('C:/Users/chris/Desktop/School/Internships/PBL/Inputs/Variable_Table.csv', delimiter = ',')

def automate_output_csv(regions,scenarios, year, baseyear, variables):
    for reg in regions:
        for sce in scenarios:
            for _,specific_var in variables.items():
                create_heatmap_baseyear_relative(year, baseyear,sce, reg, specific_var.dropna())
                
def automate_output(regions,scenarios, year, baseyear, variables):
    for reg in regions:
        for sce in scenarios:
            create_heatmap_baseyear_relative(year, baseyear,sce, reg, variables)


#automate_output_csv(out_regions, out_scenarios, '2050', '2020', variables_to_compare2)
#automate_output(out_regions, out_scenarios, '2050', '2020', variables_to_compare)

####################################################################################################################
#Checking with historical data
####################################################################################################################

              
#reading data into script

#table_2 = pd.read_csv('C:/Users/chris/Desktop/School/Internships/PBL/Inputs/all_hist_paper.csv', delimiter = ';')
#histo_data = pd.read_csv('C:/Users/chris/Desktop/School/Internships/PBL/Inputs/iamc_db.csv', delimiter =',')
             
              
#extract valuable data               
def extract_data(variable, region, year):
    year = int(year)
    
    selection = pd.DataFrame()
    for i in variable:
        pre_sel = table_2.loc[
                (table_2['variable'] == i)
                & (table_2['region'] == region)
                & (table_2['period'] == year)
            ]
        selection = selection.append(pre_sel)
    selection = selection.loc[:, ['variable', 'region', 'period', 'value']]
    return selection

def compare_models(variable, region, year, scenario):
    
    #get historical data
    comparisson = extract_data(variable, region, year)
    
    heat_map_deviations = data_prep_heat_map(year, scenario, region, variable)
    heat_map_deviations = drop_unwanted_models(heat_map_deviations)
    #create heat map data frame with the deviations in percentages
    for i in heat_map_deviations:
        heat_map_deviations.loc[:,i] = heat_map_deviations.loc[:,i] - int(comparisson.loc[comparisson['variable'] == i,'value'])
        heat_map_deviations.loc[:,i] = 100 * heat_map_deviations.loc[:,i] / abs(int(comparisson.loc[comparisson['variable'] == i,'value']))
    
    #sort the map 
    heat_map_deviations = sort_the_df(heat_map_deviations)
    
    #get colorbar to be equal to both sides
    a = heat_map_deviations.max().max()
    b = heat_map_deviations.min().min()
    
    if abs(a) > abs(b):
        colormap = abs(a)
    else: colormap = abs(b)
    
    
    #plot the heat map
    n_cols = np.arange(len(heat_map_deviations.columns))
    n_rows = np.arange(len(heat_map_deviations.index))
    plt.imshow(heat_map_deviations, cmap='RdYlGn', interpolation='none', vmin = -colormap, vmax = colormap)
   
    
    plt.title('Heatmap comparisson to historical data ' + year + ' ' + scenario +' for ' + region)
    plt.colorbar()
    plt.yticks(n_rows, heat_map_deviations.index.values)
    plt.xticks(n_cols, list(heat_map_deviations.columns.values), rotation = 'vertical')
    name_of_fig = saving_location + 'Heatmap comparisson of historical data of deviation in percentage for several variables of ' + scenario + ' in ' + year + ' in ' + region + '.png'
    plt.savefig(name_of_fig, bbox_inches='tight')
    plt.show()
    
    
def compare_models_gdp_pop(region, year,  scenario, source_gdp, source_pop):

    
    #set region names correctly
    if (region == 'CHN') or (region == 'IND') or (region == 'JPN') or (region == 'RUS') or (region == 'USA'):
        regional = 'R32' + region
    else: regional = region
    
    eu = ['R32EU15', 'R32EU12-H', 'R32EU12-M', 'HRV']
    #extract data
    comparison = pd.DataFrame()
    if region != 'EU':
        comparison['GDP|PPP'] = histo_data.loc[(histo_data['Region'] == regional) & (histo_data['Variable'] == 'GDP|PPP') & (histo_data['Scenario'] == source_gdp), year]
        comparison.iloc[0,0] = comparison.iloc[0,0] * 1.09940133
        comparison = comparison.reset_index().drop('index', axis=1)
        comparison['Population'] = histo_data.loc[(histo_data['Region'] == regional) & (histo_data['Variable'] == 'Population') & (histo_data['Scenario'] == source_pop), year].reset_index().drop('index', axis=1)
        if comparison.isnull().values.any():
            print('One or more of the criteria you enter does not have any data. Please change your criteria and try again')
            return
    #compile the region of the EU
    else:
        data = {'GDP|PPP':[0], 'Population':[0]}
        comparison = pd.DataFrame(data)
        for i in eu:
            comparison_add = pd.DataFrame()
            comparison_add['GDP|PPP'] =  histo_data.loc[(histo_data['Region'] == i) & (histo_data['Variable'] == 'GDP|PPP') & (histo_data['Scenario'] == source_gdp), year]
            comparison.iloc[0,0] = comparison.iloc[0,0] + comparison_add.iloc[0,0]
            comparison = comparison.reset_index().drop('index', axis=1)
            comparison_add['Population'] = histo_data.loc[(histo_data['Region'] == i) & (histo_data['Variable'] == 'Population') & (histo_data['Scenario'] == source_pop), year].reset_index().drop('index', axis=1).iloc[0,0]
            comparison.iloc[0,1] =  comparison.iloc[0,1] + comparison_add.iloc[0,1]
            comparison.iloc[0,0] = comparison.iloc[0,0] * 1.09940133
            if comparison.isnull().values.any():
                print('One or more of the criteria you enter does not have any data. Please change your criteria and try again')
                return
#    
    
    heat_map_deviations = data_prep_heat_map(year, scenario, region, ['GDP|PPP', 'Population'])
    heat_map_deviations = drop_unwanted_models(heat_map_deviations)
    heat_map_deviations['GDP per Capita'] = heat_map_deviations['GDP|PPP']/heat_map_deviations['Population']
    comparison['GDP per Capita'] = comparison['GDP|PPP']/comparison['Population']
    
    
    #create heat map data frame with the deviations in percentages
    for i in heat_map_deviations:
        heat_map_deviations.loc[:,i] = heat_map_deviations.loc[:,i] -int(comparison[i])
        heat_map_deviations.loc[:,i] = 100 * heat_map_deviations.loc[:,i] / abs(int(comparison[i]))
    
    #sort the map 
    heat_map_deviations = sort_the_df(heat_map_deviations)
    
    #adjust colorbar
    a = heat_map_deviations.max().max()
    b = heat_map_deviations.min().min()
    if abs(a) > abs(b):
        colormap = abs(a)
    else: colormap = abs(b)
    
    #plot the heat map
    n_cols = np.arange(len(heat_map_deviations.columns))
    n_rows = np.arange(len(heat_map_deviations.index))
    plt.imshow(heat_map_deviations, cmap='RdYlGn', interpolation='none', vmin = -colormap, vmax = colormap)
    plt.title('Heatmap comparisson to historical data ' + year + ' ' + scenario +' for ' + region)
    plt.colorbar()
    plt.yticks(n_rows, heat_map_deviations.index.values)
    plt.xticks(n_cols, list(heat_map_deviations.columns.values), rotation = 'vertical')
    name_of_fig = saving_location + 'Heatmap comparisson of historical data of deviation in percentage for population and GDP ' + scenario + ' in ' + year + ' in ' + region + '.png'
    plt.savefig(name_of_fig, bbox_inches='tight')
    plt.show()
##    
#    
#    
#    
#apply the functions
    
variable_list_2 = ['Emissions|CO2','Final Energy', 'Primary Energy']
#compare_models(variable_list_2, 'RUS', '2010', 'NPi2020_1000_VX')
#compare_models_gdp_pop('EU', '2010','INDC2030i_1000_VX', 'World Bank (WDI)', 'WUP2009')


def hist_compare(baseyear):
    for reg in out_regions:
        compare_models(variable_list_2, reg, baseyear, 'INDC2030i_1000_VX')
        compare_models_gdp_pop(reg, baseyear,'INDC2030i_1000_VX', 'World Bank (WDI)', 'WUP2009')

#hist_compare('2010')
                        

####################################################################################################################
#THE END
####################################################################################################################

                        
     
#gives an ok pop up when the run of the script is done
ctypes.windll.user32.MessageBoxW(0, "Operation Finished Successfully", "Update:", 0)