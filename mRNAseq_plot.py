import pandas as pd
from scipy import stats
from matplotlib import pyplt as plt


def plot(DGE_path, output, num1):
    '''Make plot for one of the comparison 
    Args:
        DGE_path: path to the output directory of RSEM
        output: output path for the graphs
        num1: number of samples in condition 1
    Returns:
        no returns. Save plots in the output directory
    '''
    # create output folder
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        
    # folder name without the path
    folder_name = os.path.basename(dge_path.rstrip('/'))
    
    # get the names of conditions from the folder name
    condition1, condition2 = folder_name.lstrip("DGE_").split("_vs_")
    
    trt1, trt2 = comparison
    de_file = os.path.join(opt.deliveryPath, "DE_{ftr}_{msr}_{t1}_vs_{t2}.csv".format(\
                ftr=opt.feature, msr = opt.measurement, t1=trt1, t2=trt2))
    value = pd.read_csv(de_file, index_col=[0,1])
    trt1_exp = value.ix[:,opt.treatments[trt1]]
    fig = pairwise_scatterplot(data, opt.treatments[trt1])
    fig.savefig("/home/BIOTECH/liu/tmp/scatterPlotTest.png")
    
    exp = value.ix[:,comparison]
    fig = scatter_plot(exp.values)

def probability_histogram(expr):
    '''
    Args:
        expr: list contains the 
    '''
    fig = plt.figure(figsize=(8,8))
    expr.Probability.hist(bins = 100)
    return fig

def scatter_plot(data, label=None):
    '''take two list of values and make a scatter plot 
    Args:
        data: matrix with 2 columns, each column stores expression values of one sample
        label: list twith 2 element for the sample name
    Returns:
        figure of scatter plot
    '''
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(111)
    ax.plot(data[:,0], data[:,1], '.k', alpha = 0.2, markerfacecolor='blue', markersize=5, markeredgewidth=0)
    ax.set_xlabel(comparison[0])
    ax.set_ylabel(comparison[1])
                  
    ax.set_xscale("log")
    ax.set_yscale("log")
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(data[:,0], data[:,1])
    ax.text(0.1, max(data[:,1]) * 0.9, r"$R^2={0:.2f}$".format(r_value**2), fontsize = 20, va="top")
    
    return fig

def pairwise_scatterplot(data, labels=None):
    """ Generate something similar to R `pair` 
    Take an input 'data' with multiple columns that each is one sample
    create pairwise scatter plot between data columns
    Args:
        data:  sample expression
        label: sample names
    Returns:
        R 'pair' like graph
    """
    
    # number of samples
    nSamples = data.shape[1]
    
    # size of the graph
    maxFigsize = 12
    figwidth = min(maxFigsize, 4 * nSamples)
    fig = plt.figure(figsize=(figwidth, figwidth))
    # plt.title("Pairwise comparison between replicates")
    if labels is None:
        labels = ['Sample%d'%i for i in range(nSamples)]
    for i in range(nSamples):
        for j in range(nSamples):
            nSub = i * nSamples + j + 1
            ax = fig.add_subplot(nSamples, nSamples, nSub)
            axisMax = np.amax(data[:,i] + data[:,j])
            if i == j:
                # diagnal box shows the sample label
                ax.hist(data[:,i], bins=40)
                ax.set_yscale("log")
                ax.set_xscale("log")
                ax.text(0.5, 0.9,labels[i])
            elif i > j:
                # blow diagnal shows the scatter plot
                ax.plot([0,log(axisMax)],[0,log(axisMax)], color='black', ls='-', lw = 2)
                ax.plot(data[:,i], data[:,j], '.k', alpha = 0.2, markerfacecolor='blue', markersize=2, markeredgewidth=0)
                #ax_line = fig.add_subplot(nSamples, nSamples, nSub)
                #ax.set_xlim([-0.1, axisMax])
                #ax.set_ylim([-0.1, axisMax])
                ax.set_xlim( log(axisMax))
                ax.set_ylim( log(axisMax))
                ax.set_xscale("log")
                ax.set_yscale("log")
            else:
                # above diagnal show the R^2 value
                slope, intercept, r_value, p_value, std_err = stats.linregress(data[:,i], data[:,j])
                ax.text(0.5,0.5, r"$R^2={0:.2f}$".format(r_value**2) , ha="center", va="center", fontsize = 20)
            
            # hide tick mark in the inner boxes    
            if i != nSamples - 1: plt.setp(ax.get_xticklabels(), visible=False)
            if j != 0: plt.setp(ax.get_yticklabels(), visible=False)
                
    return fig

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("DGE_path", help = "Directory that holds the DGE result of EBseq")
    parser.add_argument("output", help = "Output path")
    parser.add_argument("n", help = "Number of samples in condition 1", type=int)
    args = parser.parse_args()    
    plot(args.DGE_path, args.output, args.n)
