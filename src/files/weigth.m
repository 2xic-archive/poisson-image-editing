% as defined in equation 3 from http://www.pauldebevec.com/Research/HDR/debevec-siggraph97.pdf
function [ value ] = weigth( intensity )
    if(intensity <= 128)
        value = intensity;
    else
        value = 255 - intensity;
    end