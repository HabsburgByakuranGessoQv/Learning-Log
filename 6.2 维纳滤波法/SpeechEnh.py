from speechlib import *

def awgn(x, snr):
    snr = 10 ** (snr / 10.0)
    xpower = np.sum(x ** 2) / len(x)
    npower = xpower / snr
    return x + np.random.randn(len(x)) * np.sqrt(npower)

def SNR_Calc(I, In):
    """
    计算信号的信噪比
    :param I: 信号
    :param In: 带噪的语音信号
    信噪比计算公式：snr=10*log10(Esignal/Enoise)
    :return:
    """
    Ps = np.sum(np.power(I - np.mean(I), 2))  # 信号的能量
    Pr = np.sum(np.power(In - np.mean(In), 2))
    return 10 * np.log10(Ps / Pr)

def filpframe(x,win,inc):
    nf,len = x.shape
    nx = (nf - 1)* inc + len
    rameout = np.zeros(nx, 1)
    nwin = len(win)
    # winn = np.array(win)

    if nwin != 1:
        winx = np.tile(zip(* win),(nf,1))
        x = x/winx
        # x(find(isinf(x)))=0
        # = np.isinf(x)
        x[np.nonzero(np.isinf(x))] = 0


    sig = np.zeros((nf-1) * inc + len,1)
    for i in range(nf):
        start = (i-1)*inc + 1
        xn = zip(* x[:,1])
        sig[start:start+len-1] = sig[start:start+len+1]+xn
    frameout = sig
    return frameout


def LMS(xn, dn, M, mu, itr):
    """
    使用LMS自适应滤波
    :param xn:输入的信号序列
    :param dn:所期望的响应序列
    :param M:滤波器的阶数
    :param mu:收敛因子(步长)
    :param itr:迭代次数
    :return:
    """
    en = np.zeros(itr)  # 误差序列,en(k)表示第k次迭代时预期输出与实际输入的误差
    W = np.zeros((M, itr))  # 每一行代表一个加权参量,每一列代表-次迭代,初始为0
    # 迭代计算
    for k in range(M, itr):
        x = xn[k:k - M:-1]
        y = np.matmul(W[:, k - 1], x)
        en[k] = dn[k] - y
        W[:, k] = W[:, k - 1] + 2 * mu * en[k] * x
    # 求最优输出序列
    yn = np.inf * np.ones(len(xn))
    for k in range(M, len(xn)):
        x = xn[k:k - M:-1]
        yn[k] = np.matmul(W[:, -1], x)
    return yn, W, en

def weina_Norm(x, wlen, inc, NIS, alpha, beta):
    """
    使用维纳滤波
    :param x:输入语音信号
    :param wind:窗的类型
    :param framesize:帧长
    :param overlap:帧重叠长度
    :param NIS:无声帧帧数
    :param alpha,beta:抑制参数
    :return:
    """
    wnd = np.hamming(wlen)
    y = enframe(x, wnd, inc)                #分帧
    fn, flen = y.shape                      #fn为帧数，flen为频点数
    y_a = np.abs(np.fft.fft(y,axis=1))
    y_a2 = np.power(y_a, 2)
    Nt = np.mean(y_a2[0:NIS,:], axis=0)
    signal = np.zeros((flen))
    yw = np.zeros((fn, flen),dtype=complex)
    yt = np.zeros((fn,flen))

    for i in range(fn):               #对每一帧循环
        frame = y[i,:]
        y_fft = np.fft.fft(frame)
        y_fft2 = np.power(abs(y_fft),2)

        for k in range(flen):                       #每一帧的每一个频点循环
            if abs(y_fft2[k]) > alpha*Nt[k]:
                signal[k] =y_fft2[k] - alpha*Nt[k]
                if signal[k] < 0:
                    signal[k] = 0
            else:
                signal[k] = beta*Nt[k]

        Hw = signal/(signal+Nt)
        yw[i,:] = Hw*y_fft
        yt[i,:] = np.fft.ifft(yw[i,:])


    sig = np.zeros(int((fn-0.5) * inc + wlen))
    for i in range(fn):
        start = i * inc
        sig[start:start + flen] += yt[i, :]

    return sig

def weina_Im(x, wlen, inc, NIS, alpha):
    """
      使用维纳滤波
      :param x:输入语音信号
      :param wind:窗的类型
      :param framesize:帧长
      :param overlap:帧重叠长度
      :param NIS:无声帧帧数
      :param alpha:抑制参数
      :return:
      """
    wnd = np.hamming(wlen)

    y = enframe(x, wnd, inc)  # 分帧
    fn, flen = y.shape  # fn为帧数，flen为频点数
    y_a = np.abs(np.fft.fft(y, axis=1))
    y_a2 = np.power(y_a, 2)
    noise = np.mean(y_a2[0:NIS, :], axis=0)
    yw = np.zeros((fn, flen),dtype=complex)
    yt = np.zeros((fn, flen))

    snr_x_q = 0.97
    for i in range(fn):  # 对每一帧循环
        frame = y[i, :]
        y_fft = np.fft.fft(frame)
        y_fft2 = np.power(abs(y_fft), 2)
        snr_h = y_fft2/noise
        snr_h[(snr_h-1)<0] = 0
        snr_x = alpha*snr_x_q + (1-alpha)*snr_h
        Hw = snr_x/(1+snr_x)
        yw[i, :] = Hw * y_fft
        yt[i, :] = np.fft.ifft(yw[i, :])

    sig = np.zeros(int((fn - 0.5) * inc + wlen))
    for i in range(fn):
        start = i * inc
        sig[start:start + flen] += yt[i, :]
    return sig

def NLMS(xn, dn, M, mu, itr):
    """
    使用Normal LMS自适应滤波
    :param xn:输入的信号序列
    :param dn:所期望的响应序列
    :param M:滤波器的阶数
    :param mu:收敛因子(步长)
    :param itr:迭代次数
    :return:
    """
    en = np.zeros(itr)  # 误差序列,en(k)表示第k次迭代时预期输出与实际输入的误差
    W = np.zeros((M, itr))  # 每一行代表一个加权参量,每一列代表-次迭代,初始为0
    # 迭代计算
    for k in range(M, itr):
        x = xn[k:k - M:-1]
        y = np.matmul(W[:, k - 1], x)
        en[k] = dn[k] - y
        W[:, k] = W[:, k - 1] + 2 * mu * en[k] * x / (np.sum(np.multiply(x, x)) + 1e-10)
    # 求最优输出序列
    yn = np.inf * np.ones(len(xn))
    for k in range(M, len(xn)):
        x = xn[k:k - M:-1]
        yn[k] = np.matmul(W[:, -1], x)
    return yn, W, en


def SpectralSub(signal, wlen, inc, NIS, a, b):
    """
    谱减法滤波
    :param signal:
    :param wlen:
    :param inc:
    :param NIS:
    :param a:
    :param b:
    :return:
    """
    wnd = np.hamming(wlen)
    y = enframe(signal, wnd, inc)
    fn, flen = y.shape
    y_a = np.abs(np.fft.fft(y, axis=1))
    y_a2 = np.power(y_a, 2)
    y_angle = np.angle(np.fft.fft(y, axis=1))
    Nt = np.mean(y_a2[:NIS, ], axis=0)

    y_a2 = np.where(y_a2 >= a * Nt, y_a2 - a * Nt, b * Nt)

    y_a2sqrt = np.sqrt(y_a2)
    sig = OverlapAdd2(y_a2sqrt, y_angle, wlen, inc)

    # X = y_a2 * np.cos(y_angle) + 1j * y_a2 * np.sin(y_angle)
    # hatx = np.real(np.fft.ifft(X, axis=1))
    #
    # sig = np.zeros(int((fn - 1) * inc + wlen))
    #
    # for i in range(fn):
    #     start = i * inc
    #     sig[start:start + flen] += hatx[i, :]
    return sig

def SpectralSubIm(signal, wlen, inc, NIS, Gamma, Beta):
    wnd = np.hamming(wlen)
    y = enframe(signal, wnd, inc)
    y_fft=np.fft.fft(y, n=wlen, axis=1)
    y_angle = np.angle(y_fft[:,:int(y_fft.shape[1]/2)+1])
    Y = np.power(np.abs(y_fft[:,:int(y_fft.shape[1]/2)+1]),Gamma)
    fn, flen = Y.shape
    N = np.mean(Y[0:NIS,:],axis=0)
    NRM = np.zeros(N.shape)
    X = np.zeros((fn,flen))
    NoiseCounter = 0
    NoiseLength = 9

    YS = Y
    for i in range(1,fn-1):
        YS[i, :]=(Y[i-1, :] + Y[i, :]+Y[i+1, :]) / 3

    for i in range(fn):
        NoiseFlag, SpeechFlag, NoiseCounter, Dist = vad_LogSpec(np.power(Y[i, :],(1 / Gamma)),
                                                                np.power(N, (1 / Gamma)),
                                                                NoiseCounter)    # 基于频谱距离的VAD检测
        if SpeechFlag == 0:
            N = (NoiseLength * N + Y[i, :]) / (NoiseLength + 1)# 更新并平滑噪声
            NRM = np.maximum(NRM,YS[i, :]-N)   # 更新最大的噪声残余
            X[i, :]=Beta * Y[i, :]
        else:
            D = YS[i, :]-N   # 谱减
            if i > 1 and i < fn:     # 减少噪声残留项
                for j in range(len(D)):
                    if D[j] < NRM[j]:
                        D[j] = np.min([D[j],YS[i-1, j] - N[j],YS[i + 1, j] - N[j]])

            X[i, :]=np.maximum(D, 0)

    output = OverlapAdd2(np.power(X, (1 / Gamma)), y_angle, wlen, inc)
    return output

def vad_LogSpec(signal, noise, NoiseCounter=0, NoiseMargin=2, Hangover=8):
    """
    对数频率距离检测语音端点
    :param signal:
    :param noise:
    :param NoiseCounter:
    :param NoiseMargin:
    :param Hangover:
    :return:
    """
    SpectralDist = 20 * (np.log10(signal) - np.log10(noise))
    SpectralDist = np.maximum(SpectralDist,0)

    Dist = np.mean(SpectralDist)
    if Dist < NoiseMargin:
        NoiseFlag = 1
        NoiseCounter += 1
    else:
        NoiseFlag = 0
        NoiseCounter = 0
    if NoiseCounter > Hangover:
        SpeechFlag = 0
    else:
        SpeechFlag = 1
    return NoiseFlag, SpeechFlag, NoiseCounter, Dist


def OverlapAdd2(XNEW,y_angle,windowLen,ShiftLen):

    # if int(ShiftLen) != ShiftLen:
    #     ShiftLen=int(ShiftLen)
    ShiftLen = int(ShiftLen)
    FrameNum,FreqRes= XNEW.shape
    y_angle = [i*1j for i in y_angle]
    Spec=np.multiply(XNEW,np.exp(y_angle))

    # if windowLen%2==0:
    #     Spec1=Spec[:,1:].conjugate()
    # else:
    #     Spec1 = Spec[:, 1:-1].conjugate()
    # Spec1=Spec1[::-1]
    # Spec = np.column_stack((Spec,Spec1))

    sig=np.zeros(((FrameNum-1)*ShiftLen+windowLen))
    weight=sig
    for i in range(FrameNum-1):
        start=i*ShiftLen
        spec=np.real(np.fft.ifft(Spec[i,:], windowLen))
        sig[start:start+windowLen]=sig[start:start+windowLen] + spec
    ReconstructedSignal=sig
    return ReconstructedSignal



