# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 2021

(C) 2021, Rohde&Schwarz, ramian
"""


def ReadFile( filename):
    import rskfd

    data,fs = rskfd.ReadWv( filename)
    print( f'RMS power in file: {rskfd.MeanPower( data)} dBm, peak power: {rskfd.MeanPower( data)} dBm.\n')

if __name__ == "__main__":
	ReadFile( r'awgn_20kHz.wv')
