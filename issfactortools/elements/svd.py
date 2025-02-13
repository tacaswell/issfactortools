import numpy as np
import matplotlib.pyplot as plt


def gaussian(x, amplitude, center, sigma):
    return amplitude * np.exp(-np.power(x - center, 2) / np.power(np.sqrt(2) * sigma, 2))


def exponentialDecay(time, amplitude, tau):
    return amplitude * np.exp(-time / tau)


def creategraph(matrix, t, x, y, *args,
                fig=None):  # takes in matrix, title, xlabel, ylabel, and potenteial args to make plot
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(t)
    plt.plot(matrix)
    if args:  # potential args are number of data points to plot, oriented by colums or rows, and a label
        num, orientation, lab = args
        if fig is not None:
            plt.figure(fig.numner)
        if (orientation == "c"):
            i = 0
            for i in range(num):
                plt.plot(matrix[:, i], label=(lab + str(i + 1)))
        elif (orientation == "r"):
            i = 0
            for i in range(num):
                plt.plot(matrix[i, :], label=(lab + str(i + 1)))
        plt.legend()
    else:
        plt.plot(matrix)
    plt.show()


def getRankedMatrices(number, matrix, rcd):
    if rcd == "r":
        # print("Row")
        return matrix[:number, :]
    elif rcd == "c":
        return matrix[:, :number]
    elif rcd == "d":
        m = np.diag(matrix)
        return m[:number, :number]


def getResiduals(uN, sN, vN, A):
    An = uN @ sN @ vN
    residuals = A - An
    return An, residuals


def getChiSqS(S):
    return np.sum((S ** 2))


def getChiSq(x):
    return np.sum((x ** 2))


def plot_data(x=None, data=None, ax=None, fmt='ks-', limits=None,
              yscale='log', labels=None, plot_title='', font = None):

    if ax is None:
        _, ax = plt.subplots(111)

    if x is None:
        a, b = data.shape
        x = np.arange(a)

    ax.plot(data)



    if ax is not None:
        ax.set_title(plot_title, fontsize=font)
        if yscale:
            if limits is not None:
                #matrix = matrix[0:limits]
                print("L2: " + str(limits))
                if labels is None:
                    ax.semilogy(data[0:limits], fmt)
                else:
                    ax.semilogy(data[0:limits], fmt, label = labels)
                    ax.legend()
                ax.legend()
            else:
                if labels is None:
                    ax.semilogy(data, fmt)
                else:
                    ax.semilogy(data, fmt, label = labels)
                    ax.legend()
        else:
            if x is None:
                if limits is not None:
                    #matrix = matrix[0:limits]
                    print("L1: "+str(limits))
                    if labels is None:
                        ax.plot(data[0:limits], fmt)
                    else:
                        ax.plot(data[0:limits], fmt, label = labels)
                        ax.legend()
                    ax.legend()
                else:
                    if labels is None:
                        ax.plot(data[0:limits], fmt)
                    else:
                        ax.plot(data[0:limits], fmt, label = labels)
                        ax.legend()
                    ax.plot(data, fmt)
                    ax.legend()
            else:
                if limits is not None:
                    #matrix = matrix[0:limits]
                    print("L3: " + str(limits))
                    if labels is None:
                        ax.plot(data[0:limits], fmt)
                    else:
                        ax.plot(data[0:limits], fmt, label = labels)
                        ax.legend()
                    ax.legend()
                else:
                    if labels is None:
                        ax.plot(x, data, fmt)
                    else:
                        ax.plot(x, data, fmt, label = labels)
                        ax.legend()

    else:
        plt.figure()
        plt.title(plot_title)
        if yscale:

            ax.semilogy(data, fmt)
            ax.legend()
        else:
            if x is None:
                ax.plot(data, fmt)
                ax.legend()
            else:
                ax.plot(data, x, fmt)
                ax.legend()
        plt.show()



def getPicture(name, matrix, fig=None, font=None):
    if fig is not None:
        fig.set_title(name, fontsize=font)
        fig.imshow(matrix)
    else:
        plt.figure()
        plt.title(name)
        plt.imshow(matrix)
        plt.show()


def getSubset(startcolumns, endcolumns, matrix):
    return matrix[:, startcolumns:endcolumns]


def SVDNoise(A, noiseLevel, noise):
    noiseA = A + (noiseLevel * noise)
    u, s, v, = np.linalg.svd(noiseA)
    return noiseA, u, s, v


def LRA(uMatrix, sMatrix, vMatrix, n, A, noiseLevel=None, fig=None, font=None):
    chiSq = []
    chiSqS = []
    placeholder = np.copy(sMatrix)
    i = 1
    while i < n:
        uN = getRankedMatrices(i, uMatrix, "c")
        sN = getRankedMatrices(i, sMatrix, "d")
        vN = getRankedMatrices(i, vMatrix, "r")

        temp = np.diag(sMatrix)
        num = 0
        for num in range(i):
            placeholder[num] = 0

        chiSqS.append(getChiSqS(placeholder))
        An, residuals = getResiduals(uN, sN, vN, A)
        chiSq.append(getChiSq(residuals))

        i = i + 1
    nArr = np.arange(1, len(chiSq) + 1)
    if fig is not None:
        fig.plot(nArr, chiSq, ".-", label="Residuals")
        fig.plot(nArr, chiSqS, ".-", label="Singular Values")
        fig.legend()
        fig.set_xlabel("Rank(n)", fontsize=font)
        fig.set_ylabel("Chi Squared", fontsize=font)
        if noiseLevel is not None:
            fig.set_title("Rank vs Chi Squared for a noise level of " + str(noiseLevel), fontsize=font)
    else:
        plt.figure()
        plt.plot(nArr, chiSq, ".-", label="Residuals")
        plt.plot(nArr, chiSqS, ".-", label="Singular Values")
        plt.legend()
        plt.xlabel("Rank(n)")
        plt.ylabel("Chi Squared")
        if noiseLevel is not None:
            plt.title("Rank vs Chi Squared for a noise level of " + str(noiseLevel))

        else:
            # plt.set_text("Rank vs Chi Squared")
            pass



    return np.array(chiSqS), np.array(chiSq)


def plotsingvalues(s, fig=None, font=None):  # plot a matrix of singular values
    nArr = np.arange(1, len(s + 1))
    if fig is not None:  # if the user has passed in their own figure, use that
        print("HERE!")
        fig.semilogy(s, ".-", label="sN")
        fig.set_xlabel("Index", fontsize=font)
        fig.set_ylabel("Singular Value", fontsize=font)
        fig.legend()
        fig.set_title("Singular Values vs Index", fontsize=font)
    else:  # otherwise design a new plot for them
        print(s)
        plt.figure()
        plt.plot(s, "o-", label="sN")
        plt.xlabel("Index")
        plt.ylabel("Singular Value")
        plt.legend()
        plt.title("Singular Values vs Index")


def _getAutocorrelation(matrix, lag=1):
    autocorrelation = []
    rows, cols = np.shape(matrix)
    for i in range(cols):
        vec = matrix[:, i]
        x1 = vec[lag:]
        x2 = vec[:-lag]
        ac = np.sum(x1 * x2)
        autocorrelation.append(ac)
    return np.array(autocorrelation)

def getAutocorrelation(matrix, lag=1, title=None, fig=None, font=None):
    autocorrelation = _getAutocorrelation(matrix, lag=lag)
    rows, cols = np.shape(matrix)
    k = lag
    for i in range(cols):
        vec = matrix[:, i]
        x1 = vec[k:]
        x2 = vec[:-k]
        ac = np.sum(x1 * x2)
        autocorrelation.append(ac)

    if fig is not None:
        fig.plot(autocorrelation, "k.-")
        if title is not None:
            fig.set_title("Autocorrelation of " + title, fontsize=font)
        fig.plot([0, cols], [0.8, 0.8], color='r', linestyle='dashed')
    else:
        plt.figure()
        plt.plot(autocorrelation, "k.-")
        plt.plot([0, cols], [0.8, 0.8], color='r', linestyle='dashed')
        if title is not None:
            plt.title("Autocorrelation of " + title)


def _get_lra_chisq(s):
    chisq = (np.cumsum((s ** 2)[::-1])[::-1])[1:]
    return np.hstack((chisq, 0))



def doSVD(A):
    u, s, vT = np.linalg.svd(A)
    v = vT.T

    lra_chisq = _get_lra_chisq(s)
    ac_u = _getAutocorrelation(u)
    ac_v = _getAutocorrelation(v)

    # more methods for significance testing
    # F test etc

    return u, s, v, lra_chisq, ac_u, ac_v



def plot_svd_results(x, t, u, s, v, lra_chisq, ac_u, ac_v, figure1, figure2, energy = None, n_cmp_show=3, n_val_show = 25, font=8):

    ax_u = figure1.add_subplot(2, 1, 1)
    ax_v = figure1.add_subplot(2, 1, 2)

    ax_s = figure2.add_subplot(2, 1, 1)
    ax_ac = figure2.add_subplot(2, 1, 2)


    subsetu = getSubset(0, n_cmp_show, u)
    subsetv = getSubset(0, n_cmp_show, v)

    plot_data(x, subsetu, ax_u, fmt='-', plot_title="subset of U", font=font)  #, lab = "Componenets")  # 2
    plot_data(t, subsetv, ax_v, fmt='-', plot_title="subset of V", font=font)  #, lab = "Comp")  # 3

    plot_data(data=s, ax=ax_s, fmt='k.-', limits=n_val_show, yscale=True, labels="Singular Values",
              plot_title="Singular values", font=font)  # 7
    plot_data(data=lra_chisq, ax=ax_s, fmt='bs-', limits=n_val_show, yscale=True, labels="Chi Squared",
              plot_title="Singular values", font=font)  # 7

    plot_data(data=ac_u, ax=ax_ac, fmt='ks-', limits=n_val_show, labels="AC_U", plot_title="", font=font)  # 3
    plot_data(data=ac_v, ax=ax_ac, fmt='r.-', limits=n_val_show, labels="AC_V", plot_title="autocorrelation",
              font=font)  # 3

    # plt.tight_layout()


    #
    #     # getAutocorrelation(noiseu, 1, "u", ax4, font)  # 4
    #     # getAutocorrelation(noisev.T, 1, "v", ax5, font)  # 5
    #     LRA(noiseu, noises, noisev, len(noises) + 1, noiseA, noiseLevel, ax6, font)  # 6
    #
    # else:
    #     noiseA, noiseu, noises, noisev = SVDNoise(A, noiseLevel, noiseArray)
    #     noiseAx, u, s, v = SVDNoise(A, 0, noiseArray)
    #     print("XXXX")
    #     print(noises.shape)
    #     fullFTest(np.diag(noises), 647, 209)
    #
    #     plots("Representation of Matrix A", A)  # 1
    #
    #     subsetu = getSubset(0, 3, u)
    #     subsetnu = getSubset(0, 3, noiseu)
    #     plots("Representations of Subset of Matrix U", subsetu)
    #
    #     subsetv = getSubset(0, 3, v.T)
    #     subnoisev = getSubset(0, 3, noisev.T)
    #     plots("Representation of subset V", subsetv)
    #     getAutocorrelation(noiseu, 1, "u")
    #     getAutocorrelation(noisev.T, 1, "v")
    #     LRA(noiseu, noises, noisev, len(noises) + 1, noiseA, noiseLevel)
    #     plotsingvalues(noises)


def eigen(sValue, m):
    covariance = (sValue ** 2) / (m - 1)
    return covariance


def REV(eigen, i, m, n):
    revi = eigen / ((m - i + 1) * (n - i + 1))
    return revi


def fTest(rev, eig, k, m, n):
    bigSum = 0
    j = k - 1
    while j < n:
        bigSum += (m - j + 1) * (n - j + 1)
        j = j + 1

    littleSum = 0
    j = k + 1
    while j < n:
        # print(j)
        littleSum += eig[j]

        j = j + 1
    F = (rev / littleSum) * (bigSum)
    return F


def fullFTest(sValues, m, n):
    cov = []
    rev = []
    ans = []
    index = 0
    rows, cols = sValues.shape
    print(sValues.shape)
    while index < rows:
        cov.append(eigen(sValues[index][index], m))
        rev.append(REV(cov[index], index, m, n))
        index = index + 1

    k = 0
    while k < rows:
        ans.append(fTest(rev[k], cov, k, m, n))
        k = k + 1

    plt.figure()
    plt.plot(cov, ".-")
    plt.title("Eigen")
    plt.xlabel("Index")
    plt.ylabel("Eigenvalue")
    plt.show()
    plt.figure()
    plt.title("Rev")
    plt.xlabel("Index")
    plt.ylabel("Value")
    plt.plot(rev, ".-")
    plt.show()
    plt.figure()
    plt.plot(ans, ".-")
    plt.title("F")
    plt.xlabel("Index")
    plt.show()
    return ans

