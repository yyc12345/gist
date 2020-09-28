function freqScopeList = selfdft(timeScopeList, pointCount)
  realPointCount = length(timeScopeList);
  freqScopeList = [];
  
  for k=1:1:pointCount
    sumCache = 0;
    for n=1:1:pointCount
      if n>realPointCount
        break;
      end
      sumCache += timeScopeList(n) * exp(-i * 2 * pi * (k -1) * (n - 1) / pointCount);
    end
    freqScopeList = [freqScopeList sumCache];
  end
end
