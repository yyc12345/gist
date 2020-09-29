fft <- function(timeScopeList, M) {
    N <- 2^M
    freqScopeList <- timeScopeList[1:N]

    LH <- N/2
    J <- N/2
    if (2<=N-1) {
        for (I in seq(2, N-1, 1)) {
            if (I<J) {
                temp <- freqScopeList[I]
                freqScopeList[I] <- freqScopeList[J+1]
                freqScopeList[J+1] <- temp         
            }

            K=LH
            while(J>=K) {
                J=J-K
                K=K/2
            }
            J=J+K
        }
    }

    for (L in seq(1, M, 1)) {
        B <- 2^(L-1)
        for (J in seq(0, B-1, 1)) {
            P <- J*(2^(M-L))
            WNP <- exp(-1i * 2 * pi * P / N)
            for (k in seq(J, N-1, 2^L)) {
                temp <- freqScopeList[k+1]+freqScopeList[k+B+1]*WNP
                freqScopeList[k+B+1] <- freqScopeList[k+1]-freqScopeList[k+B+1]*WNP
                freqScopeList[k+1] <- temp
            }
        }
    }
    
    return(freqScopeList)
}

print(fft(c(1, 2, 3, 4, 5, 6, 7, 8), 3))
