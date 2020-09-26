dft <- function(timeScopeList, pointCount) {
    realPointCount <- length(timeScopeList)
    freqScopeList <- c()

    for(k in 1:pointCount) {
        sumCache <- 0
        for(n in 1:pointCount) {
            if (n>realPointCount) {
                break
            }

            sumCache <- sumCache + timeScopeList[n] * exp(-1i * 2 * pi * (k - 1) * (n - 1) / pointCount)
        }

        freqScopeList <- append(freqScopeList, sumCache)
    }

    return(freqScopeList)
}

print(dft(c(1, 2, 1, 2), 4))