function mat = segmentacion(mat,img,rgb,hsv,estRGBi,estRGBo,estHSVi,tol,step)
    %estRGBi = [maxR maxG maxB minR minG minB promR promG promB mediaR mediaG mediaB estR estG estB 
    %estHSVi = [maxH maxS maxV minH minS minV promH promS promV mediaH mediaS mediaV estH estS estV];
    
    %mat = AnalizeImgEstd(img,rgb,hsv,estRGBi,estRGBo,estHSVi,tol)
    
	szMat = size(mat,1);
    n = 1;
%     %promedios
%     r = 7;
%     g = 8;
%     b = 9;
%     s = 8;
    %media
    r = 10;
    g = 11;
    b = 12;
    s = 11;
%     %estiacion estandar
%     r = 13;
%     g = 14;
%     b = 15;
%     s = 14;
    
    promRi = mean(estRGBi(:,r));
    promGi = mean(estRGBi(:,g));
    promBi = mean(estRGBi(:,b));
    promRo = mean(estRGBo(:,r));
    promGo = mean(estRGBo(:,g));
    promBo = mean(estRGBo(:,b));
    promSi = mean(estHSVi(:,s));
    desvRi = mean(estRGBi(:,13));
    desvGi = mean(estRGBi(:,14));
    desvBi = mean(estRGBi(:,15));
    desvRo = mean(estRGBo(:,13));
    desvGo = mean(estRGBo(:,14));
    desvBo = mean(estRGBo(:,15));
    desvSi = mean(estHSVi(:,14));
    
    maxRi = promRi + desvRi; %( tol*promRi )/100;
    minRi = promRi - desvRi; %( tol*promGi )/100;
    maxGi = promGi + desvGi; %( tol*promGi )/100;
    minGi = promGi - desvGi; %( tol*promGi )/100;
    maxBi = promBi + desvBi; %( tol*promBi )/100;
    minBi = promBi - desvBi; %( tol*promBi )/100;
    
    maxRo = promRo + desvRo; %( tol*promRo )/100;
    minRo = promRo - desvRo; %( tol*promRo )/100;
    maxGo = promGo + desvGo; %( tol*promGo )/100;
    minGo = promGo - desvGo; %( tol*promGo )/100;
    maxBo = promBo + desvBo; %( tol*promBo )/100;
    minBo = promBo - desvBo; %( tol*promBo )/100;
    
    maxSi = promSi + desvSi; %( tol*promSi )/100;
    minSi = promSi - desvSi; %( tol*promSi )/100;
    
    Yo = min(mat(:,1));
    Xo = min(mat(:,2));
    Yf = max(mat(:,1));
    Xf = max(mat(:,2));
    
    
%     for Y = Yo:step:Yf
%         for X = Xo:step:Xf
%             RR = double(img(Y,X,1));
%             GG = double(img(Y,X,2));
%             BB = double(img(Y,X,3));
%             HH = hsv(Y,X,1);
%             SS = hsv(Y,X,2);
%             VV = hsv(Y,X,3);
%             
%             if( RR >= minRi & RR <= maxRi & GG >= minGi & GG <= maxGi & BB >= minBi & BB <= maxBi | SS >= minSi & SS <= maxSi )
%                 mat(n,1) = Y;
%                 mat(n,2) = X;
%                 mat(n,3) = double(img(Y,X,1));
%                 mat(n,4) = double(img(Y,X,2));
%                 mat(n,5) = double(img(Y,X,3));
%                 n = n+1;
%             end
%         end
%     end
    
%     for m = 1:1:szMat
%         y = mat(m,1);
%         x = mat(m,2);
%         
%         if(x > 1 && y > 1)
%             for i = 0:step:7
%                 for j = 0:step:7
%                     Y  = y-i;
%                     X  = x-j;
%                     RR = double(img(Y,X,1));
%                     GG = double(img(Y,X,2));
%                     BB = double(img(Y,X,3));
%                     
%                     HH = hsv(Y,X,1);
%                     SS = hsv(Y,X,2);
%                     VV = hsv(Y,X,3);
%                     
%                     if( RR >= minRi & RR <= maxRi & GG >= minGi & GG <= maxGi & BB >= minBi & BB <= maxBi | SS >= minSi & SS <= maxSi )
%                         mat(n,1) = Y;
%                         mat(n,2) = X;
%                         mat(n,3) = double(img(Y,X,1));
%                         mat(n,4) = double(img(Y,X,2));
%                         mat(n,5) = double(img(Y,X,3));
%                         n = n+1;
%                     end
%                 end
%             end
%         end
%     end

    matx = [];

    for m = 1:1:szMat
        y = mat(m,1);
        x = mat(m,2);
        
        Rm = img(y:y+7,x:x+7,1);
        Gm = img(y:y+7,x:x+7,2);
        Bm = img(y:y+7,x:x+7,3);
        
        microImg(:,:,1) = Rm;
        microImg(:,:,2) = Gm;
        microImg(:,:,3) = Bm;
        
        coord = y*1000 + x;
        index = sprintf('x%06X',coord);
        puzzle.(index) = microImg;
        
%         k = 1;
%         for i = 0:step:7
%             for j = 0:step:7
%                 matr(k,1) = y+i;
%                 matr(k,2) = x+j;
%                 matr(k,3) = Rm(i+1,j+1);
%                 matr(k,4) = Gm(i+1,j+1);
%                 matr(k,5) = Bm(i+1,j+1);
%                 k = k+1;
%             end
%         end
        
%       matx = [matx; matr];
    end
    
   mat = puzzle;
    
    display(sprintf('ventana:\nYo=%d ; Xo=%d\nYf=%d ; Xf=%d\n',Yo,Xo,Yf,Xf));
end