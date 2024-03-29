function mat = AnalizeImgEstd(img,rgb,hsv,estRGBi,estRGBo,estHSVi,tol)
    %estRGBi = [maxR maxG maxB minR minG minB promR promG promB mediaR mediaG mediaB desvR desvG desvB 
    %estHSVi = [maxH maxS maxV minH minS minV promH promS promV mediaH mediaS mediaV desvH desvS desvV];

    height = size(img,1);
    width  = size(img,2);

    if(size(estRGBi,1) > size(estRGBi,1))
        szInt = size(estRGBi,1);
    else
        szInt = size(estHSVi,1);
    end
    
    szExt = size(estRGBo,1);
    
    mat = [0 0 0 0 0];
    n   = 1;
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
%     %desviacion estandar
%     r = 13;
%     g = 14;
%     b = 15;
%     s = 14;
    
    for i=1:8:height
        for j=1:8:width
%             Rm = median(double(img(i:i+7,j:j+7,1)));
%             R  = round(median(Rm));
%             Gm = median(double(img(i:i+7,j:j+7,2)));
%             G  = round(median(Gm));
%             Bm = median(double(img(i:i+7,j:j+7,3)));
%             B  = round(median(Bm));
%             
%             Rr = median(double(rgb(i:i+7,j:j+7,1)));
%             RR = round(median(Rr));
%             Gg = median(double(rgb(i:i+7,j:j+7,2)));
%             GG = round(median(Gg));
%             Bb = median(double(rgb(i:i+7,j:j+7,3)));
%             BB = round(median(Bb));
%             
%             Hh = median(hsv(i:i+7,j:j+7,1));
%             HH = median(Hh);
%             Ss = median(hsv(i:i+7,j:j+7,2));
%             SS = median(Ss);
%             Vv = median(hsv(i:i+7,j:j+7,3));
%             VV = median(Vv);
            
            R  = double(img(i,j,1));
            G  = double(img(i,j,2));
            B  = double(img(i,j,3));
            
            RR = double(rgb(i,j,1));
            GG = double(rgb(i,j,2));
            BB = double(rgb(i,j,3));
            
            HH = hsv(i,j,1);
            SS = hsv(i,j,2);
            VV = hsv(i,j,3);
            
            inside  = false;
            outside = false;
            
            for m=1:szInt
                if(m <= size(estRGBi,1))
                    Ri = estRGBi(m,r);
                    Gi = estRGBi(m,g);
                    Bi = estRGBi(m,b);
                
                    maxRi = Ri + estRGBi(m,13); %( tol*Ri )/100;
                    minRi = Ri - estRGBi(m,13); %( tol*Ri )/100;
                    maxGi = Gi + estRGBi(m,14); %( tol*Gi )/100;
                    minGi = Gi - estRGBi(m,14); %( tol*Gi )/100;
                    maxBi = Bi + estRGBi(m,15); %( tol*Bi )/100;
                    minBi = Bi - estRGBi(m,15); %( tol*Bi )/100;
                end
                
                if(m <= size(estHSVi,1))
                    Si = estHSVi(m,s);
                
                    maxSi = Si + estHSVi(m,14); %( tol*Si )/100;
                    minSi = Si - estHSVi(m,14); %( tol*Si )/100;
                end
                
                if( RR >= minRi & RR <= maxRi & GG >= minGi & GG <= maxGi & BB >= minBi & BB <= maxBi | SS >= minSi & SS <= maxSi )                    
                    inside = true;
                    break;
                end
            end
            
            for m=1:szExt
                Ro = estRGBo(m,r);
                Go = estRGBo(m,g);
                Bo = estRGBo(m,b);
                
                maxRo = Ro + ( tol*Ro )/100;
                minRo = Ro - ( tol*Ro )/100;
                maxGo = Go + ( tol*Go )/100;
                minGo = Go - ( tol*Go )/100;
                maxBo = Bo + ( tol*Bo )/100;
                minBo = Bo - ( tol*Bo )/100;
                
                if( RR >= minRo & RR <= maxRo & GG >= minGo & GG <= maxGo & BB >= minBo & BB <= maxBo && RR+GG+BB > 0 )
                    outside = true;
                    break;
                end
            end
                
            if( inside == true & outside == false )                    
                mat(n,1) = i;
                mat(n,2) = j;
                mat(n,3) = double(R);
                mat(n,4) = double(G);
                mat(n,5) = double(B);
                n = n+1;
            end
        end
    end
        
    display('OK');
end