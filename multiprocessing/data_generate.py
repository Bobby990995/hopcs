import numpy as np
from cumxst import cumx
from cumest import cumest
import impulse_response as ir
from multiprocessing import Process
from multiprocessing import Pool

# now it can only deal with one choice of sig_tap
def signal_through_channel(sig_tap, noise_tap, i):
    signal = np.load("/home/creasy/workplace/data/exp_deviate_one_%d.npy"%(i))[:210000]
    receive = ir.moving_average(sig_tap, signal)
    # save signal snr=+inf
    np.save("temp/data_%d.npy"%(i), receive)

    # snr = 0..20 (scale from 1 to 100)
    for j in range(-10,21):
        amp = 10**(j/10.)
        white = np.random.normal(0, sqrt(sum(sig_tap)**2/amp), len(signal))
        color_scale = sqrt(sum(sig_tap)**2/amp/(sum(noise_tap)**2))
        color = ir.moving_average(noise_tap, np.random.normal(0, color_scale, len(signal)))
        np.save("temp/data_white_%d_%d.npy"%(j, i), white+receive)
        np.save("temp/data_color_%d_%d.npy"%(j, i), color+receive)


def main():
    job = Pool(8)
    r = 50
    sig_tap = [1, 0.9, 0.385, -0.771]
    noise_tap = [1, -2.33, 0.75, 0.5, 0.3, -1.41]

    for i in range(r):
        job.apply_async(signal_through_channel, args=(sig_tap, noise_tap, i))
        print "The %d Monte Carlo data prepared"%(i)

    job.close()
    job.join()

if __name__ == "__main__":
    main()


