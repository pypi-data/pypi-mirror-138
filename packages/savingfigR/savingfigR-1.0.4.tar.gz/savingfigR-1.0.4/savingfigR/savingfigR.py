# saving figures and gifs

def best_save(fig_obj, fig_name, close=True, supplemental=False):
    '''
    Save figures easily, compact, and to various places as .png (not friendly with other formats)

    INPUTS:
    fig_obj: figure object, object 
    fig_name: figure name, string 
    close: close figure, boolean 
    supplemental: put in supplemental folder, boolean 

    OUTPUT:
    Save figure in figures folder > date > main or supplemental
    '''

    # import needed library 
    import os 
    import datetime
    import matplotlib

    # current working directory 
    cwd = os.getcwd(); 

    # Does figures folder exist? 
    if os.path.exists(cwd+'/figures') == False: 
        # it doesn't exist
        # create a new figures folder 
        os.mkdir(cwd+'/figures')

    # Make figures folder the current working directory 
    os.chdir(cwd+'/figures')

    # Does current date sub folder exist 
    today = datetime.datetime.now()
    cur_day = today.strftime("%m_%d_%Y")

    # Does current date folder exist? 
    if os.path.exists(cwd+'/figures'+'/'+cur_day) == False:
        # it doesn't exist 
        # create a new date folder 
        os.mkdir(cwd+'/figures'+'/'+cur_day)

    # Make date subfolder the current working directory 
    os.chdir(cwd+'/figures'+'/'+cur_day)

    # Save in supplemental folder ?
    if supplemental:
        if os.path.exists(cwd+'/figures'+'/'+cur_day+'/'+'Supplemental') == False:
            os.mkdir(cwd+'/figures'+'/'+cur_day+'/'+'Supplemental')
        os.chdir(cwd+'/figures'+'/'+cur_day+'/'+'Supplemental')

    # Save 
    if '.png' in fig_name:
        fig_obj.savefig(fig_name, bbox_inches='tight')
    else:
        fig_obj.savefig(fig_name+'.png', bbox_inches='tight')

    if close: # close 
        matplotlib.pyplot.close(fig_obj)

    # Get back to original folder 
    os.chdir(cwd)

def writeGif(filenameG, filenames, supplemental=False, fps=25):
    '''
    Save figure files as gif file and delete figures used to create gif 

    INPUTS:
    filenameG: filename for .gif file 
    filenames: filenames of individual figures to be saved together as gif
    supplemental: put in supplemental or not, boolean

    OUTPUTS:
    .gif file of files in filenmae 
    '''
    import imageio 
    import os 
    import datetime
    import matplotlib

    # current working directory 
    cwd = os.getcwd(); 

    # Does figures folder exist? 
    if os.path.exists(cwd+'/figures') == False: 
        # it doesn't exist
        # create a new figures folder 
        os.mkdir(cwd+'/figures')

    # Make figures folder the current working directory 
    os.chdir(cwd+'/figures')

    # Does current date sub folder exist 
    today = datetime.datetime.now()
    cur_day = today.strftime("%m_%d_%Y")

    # Does current date folder exist? 
    if os.path.exists(cwd+'/figures'+'/'+cur_day) == False:
        # it doesn't exist 
        # create a new date folder 
        os.mkdir(cwd+'/figures'+'/'+cur_day)

    # Make date subfolder the current working directory 
    os.chdir(cwd+'/figures'+'/'+cur_day)

    # Save in supplemental folder ?
    if supplemental:
        if os.path.exists(cwd+'/figures'+'/'+cur_day+'/'+'Supplemental') == False:
            os.mkdir(cwd+'/figures'+'/'+cur_day+'/'+'Supplemental')
        os.chdir(cwd+'/figures'+'/'+cur_day+'/'+'Supplemental')

    with imageio.get_writer(filenameG+'.gif', mode='I', fps=fps) as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image) # add to gif 
            os.remove(filename) # delete individual 
    
    # Get back to original folder 
    os.chdir(cwd)