from symengine import exp, sqrt, Symbol 
from jitcode import y, t, jitcode
import numpy as np
from networkx import watts_strogatz_graph, erdos_renyi_graph, barabasi_albert_graph, to_numpy_matrix
from numpy.random import choice, normal



def cantor(n : int , startpoint : float, endpoint : float) -> list:
    """ Create the complete array of the Cantor set

    Parameters
    ----------
    startpoint, endpoint :                  start- and endpoint of the complete Cantor set
    n :                                     number of iterations
    
    Returns
    -------
    list :                                  1d list of the Cantor set

    References
    ----------

    """
    return [startpoint] + cant(startpoint, endpoint, n) + [endpoint]


def cant(x : float, y : float, n : int) -> list:
    """This function creates a Cantor set which mimic a fragmented barrier.

    Parameters
    ----------
    x,y :                                   start- and endpoint of the remaining parts of the Cantor set
    n :                                     number of iterations
    
    Returns
    -------
    list :                                  1d list of the remaining parts

    References
    ----------
    
    """
    if n == 0:
        return []
    new_pts = [2.*x/3. + y/3., x/3. + 2.*y/3.]
    return cant(x, new_pts[0], n-1) + new_pts + cant(new_pts[1], y, n-1)


def create_cantor(number_of_iterations : int, startpoint : float, endpoint : float) -> list:
    """ Iterative generation the n-th order Cantor set.

    Parameters
    ----------
    number_of_iterations :                  number of iterations
    startpoint, endpoint :                  start- and endpoint of the remaining parts of the Cantor set
    
    Returns
    -------
    list :                                  1d list of the n-th order Cantor set

    References
    ----------

    """
    data = []
    for n in range(number_of_iterations):
        data = cantor(n, startpoint, endpoint) 
    return data


def GiveNumberOfElement(a : list, z : float) -> int:
    """ Returns an index of an array for a given number

    Parameters
    ----------
    a :                                     an arbitrary array
    z :                                     arbitrary number in the range of the array
    
    Returns
    -------
    i :                                     index of the array where the number z is between the i-th and (i+1)-th index of the array

    References
    ----------

    """

    for i in range(len(a)-1):
        if(a[i] < z < a[i+1]):
            return i


def find_max(x : float, peak_height : float, time : int) -> tuple([int, float]):
    """ tracks all high-amplitude oscillations which are larger than a threshold 

    Parameters
    ----------
    x :                                     list of data 
    peak_height :                           threshold
    time :                                  time point

    Returns
    -------
    time :                                  return time point at which the high-amplitude oscillations is larger than the threshold
    x[-2] :                                 return the amplitude of the high-amplitude oscillations

    References
    ----------

    """

    if (x[-2] > peak_height and x[-3] < x[-2] and x[-2] > x[-1]):
        return time, x[-2]


def calculate_diff(a):
    """ Calculate difference of the elements in an array 

    Parameters
    ----------
    a :                                     arbitrary array

    Returns
    -------
    list                                    return a list with the difference between the elements of an array

    References
    ----------

    """
    return [(a[i+1]-a[i])/2+a[i] for i in range(len(a)-1)]


def sign_change(before_gamma : int, z : float, lower_threshold : float, upper_threshold : float, random : bool = True ) -> int:
    """ changes the sign of the coupling functions whether at random or state-depentent.

    Parameters
    ----------
    before_gamma :                          is the sign of the parameter before it is changed
    z :                                     position in the potential landscape 
    lower_threshold, upper_threshold :      threshold for the lower or upper state at which the sign of gamma is changed
    random :                                chose between state-dependent or random (default) switching depending on the sign of the coupling
    
    Returns
    -------
    gamma :                                 sign of the coupling

    References
    ----------

    """

    if random:
        gamma = choice([-1,1])  
    else:
        gamma = before_gamma
        if (z[-1] > upper_threshold):
            gamma = -1
        elif (z[-1] < lower_threshold):
            gamma = 1   
    return gamma

def make_control_pars(k_int2 : float, k_b : float, gamma : int, fb : int, n : int) -> list:
    """ Makes a list of all symbolic expressions for the coupling strengths, the sign of the coupling, the steepness within the Cantor set and the amplitude,
        mu and sigma of each Gaussian function

    Parameters
    ----------
    a :                                     list of symbolic expressions for the amplitude, mu and sigma

    Returns
    -------
    control_para :                          list of control parameter which can be changed during integration

    References
    ----------

    """
    control_para = [k_int2, k_b, gamma, fb]
    a = jit_function(n)
    for i in range(len(a)):
        control_para.append(a[i])
    return list(control_para)


def create_network(N : int, m : int, p : float, Ntype : str = "ws") -> np.matrix:
    """ Generates a network for Watts-Strogatz, Erdos-Renyi or Barabasi-Albert

    Parameters
    ----------
    N :                                     total number of nodes
    m :                                     number of connected nodes
    p :                                     probability for rewiring/creation of a new edge
    Ntype :                                 type of network (ws : Watts-Strogatz, er : Erdos-Renyi, ba : Barabasi-Albert)

    Returns
    -------
    A :                                     2d array for the adjacency matrix of the network 

    References
    ----------

    """

    if Ntype == "ws":
        A = watts_strogatz_graph(N, m, p)
    if Ntype == "er":
        A = erdos_renyi_graph(N,p)
    if Ntype == "ba":
        A = barabasi_albert_graph(N,m)
    A = to_numpy_matrix(A)
    return A


def jit_function(n : int) -> tuple:
    """ functions which calls symbolic expressions up to 10 Gaussian functions

    Parameters
    ----------
    n :                                     number of potential wells 

    Returns
    -------
    amp1, mu1, var1, ... :                  symbolic expression of n number of potential wells

    References
    ----------

    """
    amp1 = Symbol('amp1')
    mu1 = Symbol('mu1')
    var1 = Symbol('var1')
    amp2 = Symbol('amp2')
    mu2  = Symbol('mu2')
    var2 = Symbol('var2')
    amp3 = Symbol('amp3')
    mu3  = Symbol('mu3')
    var3 = Symbol('var3')
    amp4 = Symbol('amp4')
    mu4  = Symbol('mu4')
    var4 = Symbol('var4')
    amp5 = Symbol('amp5')
    mu5  = Symbol('mu5')
    var5 = Symbol('var5')
    amp6 = Symbol('amp6')
    mu6  = Symbol('mu6')
    var6 = Symbol('var6')
    amp7 = Symbol('amp7')
    mu7  = Symbol('mu7')
    var7 = Symbol('var7')
    amp8 = Symbol('amp8')
    mu8  = Symbol('mu8')
    var8 = Symbol('var8')
    amp9 = Symbol('amp9')
    mu9  = Symbol('mu9')
    var9 = Symbol('var9')
    amp10 = Symbol('amp10')
    mu10  = Symbol('mu10')
    var10 = Symbol('var10')
    

    if n == 1:
        return amp1, mu1, var1
    if n == 2:
        return amp1, mu1, var1, amp2, mu2, var2
    if n == 3:
        return amp1, mu1, var1, amp2, mu2, var2, amp3, mu3, var3
    if n == 4:
        return amp1, mu1, var1, amp2, mu2, var2, amp3, mu3, var3, amp4, mu4, var4
    if n == 5:
        return amp1, mu1, var1, amp2, mu2, var2, amp3, mu3, var3, amp4, mu4, var4, amp5, mu5, var5
    if n == 6:
        return amp1, mu1, var1, amp2, mu2, var2, amp3, mu3, var3, amp4, mu4, var4, amp5, mu5, var5, amp6, mu6, var6
    if n == 7:
        return amp1, mu1, var1, amp2, mu2, var2, amp3, mu3, var3, amp4, mu4, var4, amp5, mu5, var5, amp6, mu6, var6, amp7, mu7, var7
    if n == 8:
        return amp1, mu1, var1, amp2, mu2, var2, amp3, mu3, var3, amp4, mu4, var4, amp5, mu5, var5, amp6, mu6, var6, amp7, mu7, var7, amp8, mu8, var8
    if n == 9:
        return amp1, mu1, var1, amp2, mu2, var2, amp3, mu3, var3, amp4, mu4, var4, amp5, mu5, var5, amp6, mu6, var6, amp7, mu7, var7, amp8, mu8, var8, amp9, mu9, var9
    if n == 10:
        return amp1, mu1, var1, amp2, mu2, var2, amp3, mu3, var3, amp4, mu4, var4, amp5, mu5, var5, amp6, mu6, var6, amp7, mu7, var7, amp8, mu8, var8, amp9, mu9, var9, amp10, mu10, var10
    else:
        raise Exception("symbolic expressions error")



def check_length_list(n : int, a : list, b : list, c : list) -> None:
    """ checks whether all list have the same length

    Parameters
    ----------
    a, b, c :                               three arbitrary lists 

    Returns
    -------

    References
    ----------

    """
    if np.shape(a)== np.shape(b) == np.shape(c):
        check_number = np.shape(a)
        if n == check_number:
            pass
    else:
        raise Exception("The length of control parameters for the potential landscape is different!\nPlease check the parameters of the landscape.")

    
def check_length_cantor(a : list) -> None:
    """ checks whether a list is in the right format

    Parameters
    ----------
    a :                                     an arbitrary list

    Returns
    -------

    References
    ----------

    """

    number_cantor, _ = np.shape(a)
    for i in range(number_cantor):
        if a[i][0]> a[i][1]:
            raise Exception("The startpoint {} of the Cantor is larger than the endpoint {}".format(a[i][0], a[i][1]))


def check_list(now : int, amp : list, mu : list, var : list, k_int2_list : list, k_b_list : list, fragment_barrier_position : list) -> None:
    """ checks the length of all lists

    Parameters
    ----------
    amp, mu, var :                          list for amplitude, mean and variance of the Gaussian function
    k_int2_lst, k_b_lst :                   list for global coupling strength for network 2 / between network 1 and network 2
    fragment_barrier_position :             list for start- and endposition of the fragmented barriers

    Returns
    -------

    References
    ----------

    """
    check_length_list(now, amp, mu, var)
    check_length_list(now, amp, k_int2_list, k_b_list)
    check_length_cantor(fragment_barrier_position)


def initialize_amp(n : int) -> list:
    """ return all symbolic expressions for the amplitude up to 10 potential wells

    Parameters
    ----------
    n :                                     number of potential wells 

    Returns
    -------
    all_amp[:n]                             n-th number of symbolic expressions

    References
    ----------

    """
    all_amp = [Symbol('amp1'), Symbol('amp2'), Symbol('amp3'), Symbol('amp4'), Symbol('amp5'), Symbol('amp6'), Symbol('amp7'), Symbol('amp8'), Symbol('amp9'), Symbol('amp10')]
    return all_amp[:n]

def initialize_mu(n : int) -> list:
    """ return all symbolic expressions for the mu up to 10 potential wells

    Parameters
    ----------
    n :                                     number of potential wells 

    Returns
    -------
    all_mu[:n]                              n-th number of symbolic expressions

    References
    ----------

    """
    all_mu = [Symbol('mu1'), Symbol('mu2'), Symbol('mu3'), Symbol('mu4'), Symbol('mu5'), Symbol('mu6'), Symbol('mu7'), Symbol('mu7'), Symbol('mu9'), Symbol('mu10')]
    return all_mu[:n]

def initialize_var(n : int) -> list:
    """ return all symbolic expressions for the variance up to 10 potential wells

    Parameters
    ----------
    n :                                     number of potential wells 

    Returns
    -------
    all_var[:n]                             n-th number of symbolic expressions

    References
    ----------

    """
    all_var = [Symbol('var1'), Symbol('var2'), Symbol('var3'), Symbol('var4'), Symbol('var5'), Symbol('var6'), Symbol('var7'), Symbol('var8'), Symbol('var9'), Symbol('var10')]
    return all_var[:n]

def symbol_potential(n : int) -> tuple:
    """ symbolic expression of the control parameters of the potential landscape

    Parameters
    ----------
    n :                                     number of wells

    Returns
    -------
    amp, mu, var :                          returns the symbolic expression for the amplitude, mean and variance for each well in the the potential landscape

    References
    ----------
    
    """
    amp = initialize_amp(n)
    mu = initialize_mu(n)
    var = initialize_var(n)
    return amp, mu, var


def symbol_dynamics() -> tuple:
    """ symbolic expression of the control parameters of the dynamcis

    Parameters
    ----------

    Returns
    -------
    k_int2, k_b, gamma, fb :               returns the symbolic expression for parameter of the coupling strengths, the switching and the positions of the fragmented barriers

    References
    ----------
    
    """
    k_int2 = Symbol('k_int2')
    k_b    = Symbol('k_b'   )
    gamma  = Symbol('gamma' )
    fb     = Symbol('fb'    )
    return k_int2, k_b, gamma, fb

def potential(z : float, amp : list, mu : float, sigma : float) -> float:
    """succession of Gaussian function

    Parameters
    ----------
    z :                                     position in the potential landscape
    amp, mu, sigma :                        control parameters of each Gaussian functions for the amplitude, mu and sigma
    
    Returns
    -------
    float :                                 potential landscape as succession of Gaussian functions

    References
    ----------

    """

    landscape = 0
    for i in range(len(amp)):
        landscape += (
            -amp[i]/(np.sqrt(2*np.pi*sigma[i]**2))*np.exp(-(z-mu[i])**2/(2*sigma[i]**2))
        )
    return landscape


def test_potential(z : float, amp : list, mu : list, sigma : list) -> None:
    """ tests if the dynamics is larger than the potential landscape.

    Parameters
    ----------
    z :                                     position in the potential landscape
    amp, mu, sigma :                        control parameters of each Gaussian functions for the amplitude, mu and sigma
    
    Returns
    -------
    array :                                 potential landscape as succession of Gaussian functions

    References
    ----------

    """
    landscape = potential(z,amp,mu, sigma)
    if landscape >= -1e-2:
        raise Exception("Unbounded dynamics outside of the potential landscape.\nModify the potential landscape!")



def potential_derivative(z : float, amp : list, mu : list, sigma : list) -> float:
    """ derivative of the potential landscape.

    Parameters
    ----------
    z :                                     position in the potential landscape
    amp, mu, sigma :                        control parameters of each Gaussian functions for the amplitude, mu and sigma
    
    Returns
    -------
    float :                                 potential landscape as succession of Gaussian functions

    References
    ----------

    """

    landscape = 0
    for i in range(len(amp)):
        landscape += (
            (z-mu[i])/sigma[i]**2*amp[i]/(np.sqrt(2*np.pi*sigma[i]**2))*np.exp(-(z-mu[i])**2/(2*sigma[i]**2))
        )
    return landscape


def plot_potential(amp : list, mu : list, sigma : list, fb_position : list, steepness : float) -> list:
    """ returns y-value of the potential landscape.

    Parameters
    ----------
    z :                                     position in the potential landscape
    amp, mu, sigma :                        control parameters of each Gaussian functions for the amplitude, mu and sigma
    fb_position :                           position for Cantor set or noise of the fragmented barriers 
    steepness :                             steepness of the fragmented barrier segments
    
    Returns
    -------
    array :                                 y-value of potential landscape as succession of Gaussian functions

    References
    ----------

    """

    number_cantor, _ = np.shape(fb_position)

    fb_pos = [create_cantor(4, fb_position[i][0], fb_position[i][1]) for i in range(number_cantor)]

    fb = 0


    fb = Symbol("fb")
    b = Symbol("b")

    def superposition_gauss():
        dZdt = 0
        for i in range(len(amp)):
            dZdt += (
            -amp[i]*(t-mu[i])/(sigma[i] )**2*1/(sqrt(2*np.pi*(sigma[i] )**2))*exp(-(t-mu[i])**2/(2*(sigma[i] )**2))*b
            )
        dZdt += fb
        yield dZdt


    Ip = jitcode(
        superposition_gauss,
        control_pars=[fb, b],
        verbose = False
    )



    Ip.set_integrator("dopri5")
    initial = [0.0]
    Ip.set_initial_value(initial, time = -10.0+min(mu))

    y_value = []
    times_begin = min(mu) - 10
    times_end = max(mu) + 10
    times = np.arange(times_begin, times_end, 0.05)
    for time in times:
        for i in range(number_cantor):
            b = 1
            fb = 0
            if fb_pos[i][0] < time < fb_pos[i][-1]:
                fb =  cantor_slope(time, fb_pos[i], steepness, amp, mu, sigma)
                # fb =  noise_slope(time, fb_pos[i], amp, mu, sigma)
                break
            else:
                b = 1
                fb = 0

        Ip.set_parameters(fb, b)
        y_value.append(-1*Ip.integrate(time))

    return y_value


def cantor_slope(z : float, cantor : list, steepness : float, amp : float, mu : float, sigma : float) -> float:
    """ Modifying the steepness within the fragmented barriers

    Parameters
    ----------
    z :                                     position in the potential landscape 
    cantor :                                list with Cantor set
    steepness :                             steepness in the Cantor set
    amp, mu, sigma :                        control parameters of each Gaussian functions for the amplitude, mu and sigma (list)

    Returns
    -------
    fb :                                    steepness for each element in the Cantor set

    References
    ----------

    """
    j = GiveNumberOfElement(cantor, z)
    if (j>=len(cantor)-2):
        fb = 0 + potential_derivative(z, amp, mu, sigma)
    elif(j%2 == 0):
        fb = steepness * 1/np.diff(cantor)[j] + potential_derivative(z, amp, mu, sigma)
    elif(j%2 == 1):
        fb = steepness * -1/np.diff(cantor)[j] + potential_derivative(z, amp, mu, sigma)
    return fb


def noise_slope(z : float, cantor : list, amp : list, mu : list, sigma : list) -> float:
    """ Modifying the steepness within the fragmented barriers by making the barriers noisy

    Parameters
    ----------
    z :                                     position in the potential landscape 
    cantor :                                list with Cantor set
    amp, mu, sigma :                        control parameters of each Gaussian functions for the amplitude, mu and sigma (list)

    Returns
    -------
    fb :                                    steepness for each element in the Ornstein-Uhlenbeck process

    References
    ----------

    """
    t, xs = Ornstein_Uhlenbeck(cantor, 0.1, 0.3, 0.01)
    j = GiveNumberOfElement(t, z)
    fb = xs[j] + potential_derivative(z, amp, mu, sigma)
    return fb


def Ornstein_Uhlenbeck(position : list, theta : float, sigma : float, delta_t : float) -> tuple([list,list]):
    """ Generation of a one-dimensional Ornstein-Uhlenbeck process.

    Parameters
    ----------
    position :                              position in the potential landscape 
    theta/sigma :                           drift/diffusion term of Ornstein-Uhlenbeck process
    delta_t :                               time step of integration

    Returns
    -------
    time :                                  integration time
    y :                                     time series of Ornstein-Uhlenbeck process

    References
    ----------

    """
    time = np.linspace(min(position), max(position), int(abs(max(position)-min(position))*10))

    y = np.zeros([time.size])
    dW = np.random.normal(loc = 0, scale = delta_t, size = [time.size,1])
    y[0] = np.random.normal(size = 1)/10

    for i in range(1,time.size):
        y[i]  = y[i-1] - theta * y[i-1] * delta_t + sigma * dW[i]
    return time, y


def coupling_to_potential(now : int, amp : float, mu : float, var : float, Z : float , fb : float, gamma : int, X : float, N : int):
    """ Coupling function of the mean field of the FHN dynamics to the potential landscape which is a succession of Gaussian functions.

    Parameters
    ----------
    
    Returns
    -------
    dZdt :                                 ODE for the coupling in the potential landscape

    References
    ----------

    """

    dZdt = 0
    for i in range(now):
        dZdt += (
        -amp[i]*(Z-mu[i])/sqrt(var[i])**2/(sqrt(2*np.pi*sqrt(var[i])**2))*exp(-(Z-mu[i])**2/(2*sqrt(var[i])**2))
        )
    dZdt += fb
    M     = gamma * sum(X(i,0)+X(i,1) for i in range(N))/N
    dZdt +=  M*(0.6 + 0.01*Z)
    return dZdt



def white_noise(noise : bool) -> float:
    """ Generate white noise from a normal distribution at the position of loc and a width of scale.
    
    Parameters
    ----------
    noise :                                 if noise == True -> random number, if noise == False -> no noise
    
    Returns
    -------
    noise :                                 random number from the normal distribution or 0

    References
    ----------

    """
    if noise:
        return normal(loc = 0, scale = 1e-6, size = 1)[0]
    else:
        return 0


def x_component(X, Y, i : int, q : int, a : float, N : int, k_int1 : float, k_int2 : float, k_b : float, Sym : list, S : np.ndarray, B : list, noise : bool = False):
    """ ODE of the x-components of the FitzHugh-Nagumo netowrk of neworks

    Parameters
    ----------
    X, Y :                                  x- and y-component of the FitzHugh-Nagumo oscillators
    i, q :                                  i-th oscillator in network q
    a :                                     control parameter of the FitzHugh-Nagumo oscillators
    N :                                     number of oscillators in each network
    k_int1, k_int2 :                        global coupling strength in network 1, network 2
    k_b :                                   global coupling strength between network 1 and 2
    Sym :                                   symbolic expression for repeating expressions of the ODEs
    S :                                     adjacency matrix for network 1 and 2
    B :                                     adjacency matrix for network of networks
    noise :                                 noise can be added to the dynamics of X and Y

    Returns
    -------
    dXdt :                                  returns the x-component for i-th oscillator in network q

    References
    ----------
    
    """

    dXdt = (X(i,q)
                    * (a -X(i,q))
                    * (X(i,q)-1.0)
                    - Y(i,q)
                )
    coupling_sum_W = sum(
            X(j,q)-X(i,q)
            for j in range(N)
            if S[i,j]
        )
    if q == 0:
        k_W = k_int1
    else:
        k_W = k_int2
    dXdt += k_W/(N-1) * coupling_sum_W
    coupling_sum_B = sum(
            Sym[r]-N*X(i,q)
            for r in [0,1]
            if B[q][r]
        )
    dXdt += k_b/N * coupling_sum_B
    dW = white_noise(noise)
    dXdt += dW
    return dXdt


def y_component(X, Y, i : int, q : int, b : float, c : float, noise : bool = False):
    """ ODE of the y-components of the FitzHugh-Nagumo netowrk of neworks

    Parameters
    ----------
    X, Y :                                  x- and y-component of the FitzHugh-Nagumo oscillators
    i, q :                                  i-th oscillator in network q
    b, c :                                  control parameters of the FitzHugh-Nagumo oscillators
    noise :                                 noise can be added to the dynamics of X and Y

    Returns
    -------
    dYdt :                                  returns the y-component for i-th oscillator in network q

    References
    ----------
    
    """
    dW = white_noise(noise)
    return b[i] * X(i,q) - c * Y(i,q) + dW


def return_set_pa(k_int2 : float, k_b2 : float, gamma2 : int, fb2 : float, amp : list, mu : list, var : list) ->tuple([list, list, list, list]):
    """ returns all control parameters and assign a number to the symbolic expression a

    Parameters
    ----------
    k_int2, k_b2 :                      coupling constants within sub-network 2 and between sub-network 1 and 2
    gamma2 :                            sign of the coupling
    fb2 :                               steepness of the fragmented barrier
    amp, mu, var :                      control parameters of the potential landscape which can be changed during integration

    Returns
    -------
    set_new_pa :                        list of all control parameters
    names_amp[:len(amp)] :              list of the control parameters of the amplitude
    names_mu[:len(mu)] :                list of the control parameters of the mu
    names_var[:len(var)] :              list of the control parameters of the variance

    References
    ----------

    """

    k_int2 = float(k_int2)
    k_b = float(k_b2)
    gamma = float(gamma2)
    fb = float(fb2)
    amp1, amp2, amp3, amp4, amp5, amp6, amp7, amp8, amp9, amp10 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    mu1, mu2, mu3, mu4, mu5, mu6, mu7, mu8, mu9, mu10 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    var1, var2, var3, var4, var5, var6, var7, var8, var9, var10 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    names_amp = [amp1, amp2, amp3, amp4, amp5, amp6, amp7, amp8, amp9, amp10]
    names_mu = [mu1, mu2, mu3, mu4, mu5, mu6, mu7, mu8, mu9, mu10]
    names_var = [var1, var2, var3, var4, var5, var6, var7, var8, var9, var10]
    set_new_pa = [k_int2, k_b, gamma, fb]
    for i in range(len(amp)):
        names_amp[i] = amp[i]
        names_mu[i] = mu[i]
        names_var[i] = var[i]
        set_new_pa.append(amp[i])
        set_new_pa.append(mu[i])
        set_new_pa.append(var[i])

    return set_new_pa, names_amp[:len(amp)], names_mu[:len(mu)], names_var[:len(var)]


def prepare_jitcode(ODE_f, helpers, nos : int, control_para : list):
    """ setup the integrator from the module jitcode
    Parameters
    ----------
    ODE_f :                                 system of ODEs
    helpers :                               define repeating expressions for the ODEs
    nos :                                   number of oscillators in each network
    control_para :                          all control parameter, which can be changed during integration

    Returns
    -------
    I :                                     integrator
   
    References
    ----------

    """
    I = jitcode(
            ODE_f,
            helpers=helpers,
            n = (4*nos+1),
            control_pars= control_para, 
            verbose = False
        )
    
    I.set_integrator('dopri5')
    return I


def create_dynamic_variables(nos : int) -> tuple:
    """ initialize the dynamical variavles for x- and y-components of the FitzHugh-Nagumo oscillators and for the motion in the potential landscape
    Parameters
    ----------
    nos :                                   number of oscillators in each network 

    Returns
    -------
    X, Y, Z :                               x-, y-, and z-component of the ODEs 
    Sym :                                   symbolic expression for the helpers
    helpers :                               define repeating expressions for the ODEs
   
    References
    ----------

    """
    X = lambda i,q: y(  q*2*nos+i)
    Y = lambda i,q: y(nos+q*2*nos+i)
    Z = y(4*nos)

    Sym = [Symbol('S_0'), Symbol('S_1')]
    helpers = [
            (Sym[q],sum(X(i,q) for i in range(nos)))
            for q in [0,1]
        ]
    return X, Y, Z, Sym, helpers


    