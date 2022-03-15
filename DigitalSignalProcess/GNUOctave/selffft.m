function freqScopeList = selffft(timeScopeList, M)
  N = 2 ^ M;
  freqScopeList = timeScopeList(1:end);
  
  % construct butterfly struct
  LH=N/2;
  J=N/2;
  for I=1:1:N-2
    if I < J
      temp=freqScopeList(I + 1);
      freqScopeList(I + 1)=freqScopeList(J + 1);
      freqScopeList(J + 1)=temp;
    end
    
    K=LH;
    while J>=K
      J=J-K;
      K=K/2;
    end
    J=J+K;
  end
  
  % calc butterfly
  for L=1:1:M
    B = 2 ^ (L - 1);
    for J=0:1:B-1
      P=J*(2^(M-L));
      WNP=exp(-i * 2 * pi * P / N);
      for k=J:2^L:N-1
        temp=freqScopeList(k+1)+freqScopeList(k+B+1)*WNP;
        freqScopeList(k+B+1)=freqScopeList(k+1)-freqScopeList(k+B+1)*WNP;
        freqScopeList(k+1)=temp;
      end
    end
  end
end
