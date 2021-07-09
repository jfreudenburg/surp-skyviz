; The 2MASS Redshift Survey
; Huchra et al., ApJS, in press
;
; http://tdc-www.harvard.edu/2mrs/
; catalog version 2.4, 2011 Dec 16
; maintained by Lucas Macri, lmacri@tamu.edu
;
; This routine will read the ASCII catalog contents into a structure
; called "g" with "ng" items and generate a "hockey puck" plot as
; described in the paper.

pro hockeypuckplot

a={id:'',r:0.,d:0.,l:0.,b:0.,k:0.,h:0.,j:0.,kt:0.,ht:0.,jt:0.,ek:0.,eh:0.,ej:0.,ekt:0.,eht:0.,ejt:0.,ebv:0.,ri:0.,rt:0.,ba:0.,cf:'',t:'',ts:'',v:0l,ev:0,vc:'',vsrc:'',catid:''}
frm='(A16,4(F10.5),6(F7.3),10(F6.3),1x,A4,1x,A5,1x,A2,I7,I4,1x,A1,1x,A19,1x,A)'

g=replicate(a,45000)
ng=0l
line=''
openr,lun,'../catalog/2mrs_1175_done.dat',/get_lun
for j=0l,8 do $
 readf,lun,line
while not eof(lun) do begin
 readf,lun,a,format=frm
 g(ng)=a
 ng++
endwhile
close,lun
free_lun,lun
ng--
g=g(0:ng)

print,'Catalog has been read...'

print,'Number of entries is ',ng
  
print,'Now calling hockeypuck'

;  window,xs=830,ys=800
  set_plot,'ps'
  device,filename='hockeypuck.ps', xsize=8.44, ysize=8,/inches

;  hockeypuck,g.r,g.d,g.v,15000,8000,'North' 
  hockeypuck,g.r,g.d,g.v,15000,8000,'South' 

return
end

pro hockeypuck,ra,dec,v,l1,l2,hemi

;-------------------------------------------------------------
;+
; NAME:
;       HOCKEYPUCK
; PURPOSE:
;       make Hockey Puck diagrams of redshift surveys
;       (as described in Huchra et al. 2011)
;       
; CALLING SEQUENCE:
;       hockeypuck,ra,dec,v,l1,l2,hemi
;
; INPUTS:
;       RA and Dec should be entered in decimal degrees
;       v is the recessional velocity in km/s
;       l1 and l2 are the size of the Hockey puck cylinder. l1>l2. For
;       example in Huchra et al. (2011) we use l1=15000km/s and l2=8000km/s
;       hemi is a code indicating if you want North or South
;       hemisphere. Please enter 'North', or 'South'. 
;       
; KEYWORD PARAMETERS:
;       Keywords:
;       /SOUTH southern hemisphere. Otherwise does the North.
;       (not yet implemented)
; OUTPUTS:
;       hockeypuck plot printed to device     out
; USES:
;       polrec
; NOTES:
; MODIFICATION HISTORY:
;       2011 created by Karen L. Masters
;
; This software may be used, copied, or redistributed as long as it is not
; sold.  This routine is provided as is without any express or implied warranties
; whatsoever. If you use this code please cite the description of Hockey Puck
; diagrams provided in Huchra et al. (2011). 
;
;-------------------------------------------------------------
 
  print,'Number of entries is ',n_elements(ra)

  if (hemi eq 'North') then begin
     find=where(dec ge 0 and v*cos(!pi*dec/180.) le l1 and v*sin(!pi*dec/180.) le l2,count)    
  endif else begin
     if (hemi eq 'South') then begin
        find=where(dec le 0 and v*cos(!pi*dec/180.) le l1 and v*sin(!pi*dec/180.) le l2,count)
     endif else print, "Please enter the hemisphere as 'North' or 'South'"
  endelse

  print,'Number in hemisphere within Hockey puck cylinder is: ',count

   ra=ra[find]
   dec=dec[find]
   v=v[find]

   r=v*cos(!pi*dec/180.)
; Want zero degrees to point down, so substract 90 deg from the angles
   a=!pi*(ra-90)/180.
   
   ;polrec,r,a,x,y
   
; Plot circles at the two redshift limits.
   c=!pi*(1.+findgen(361))/180.
   r1=l1*c/c
   r2=l2*c/c

; Tick marks every hour in RA. With 0h at the bottom.  
   cl=!pi*(15.*findgen(24)-90.)/180.
   o=cl*180./!pi

   ralabels=['0h','1h','2h','3h','4h','5h','6h','7h','8h','9h','10h','11h','12h','13h','14h','15h','16h','17h','18h','19h','20h','21h','22h','23h']

   subtitle=hemi+'ern Hemisphere'

   range=l1+l1/50.

   plotsym,0,0.2,/fill
   plot,/polar,r,a,psym=8,xstyle=5,ystyle=5,xrange=[-range,range],yrange=[-range,range],charsize=1.5,thick=2
   oplot,r1,c,/polar,thick=2
   oplot,r2,c,/polar,thick=2

; Check orientation of plot.
;   oplot,[l1,l2],[-90*!pi/180.,-90*!pi/180.],/polar

; Labels around the outer circle
   rl=r1+l1/25.
   angle=(o+270) mod 360
   polrec,rl,cl,xl,yl
;   xyouts,xl,yl,ralabels,/data,alignment=0.5,charsize=1.
   
 ; Tick marks and labels around outer circle
   rin=r1-l1/50.
   rout=r1+l1/50.
   polrec,rin,cl,x1,y1
   polrec,rout,cl,x2,y2

   for i=0,23 do begin
      oplot,[x1[i],x2[i]],[y1[i],y2[i]]
      xyouts,xl[i],yl[i],ralabels[i],/data,alignment=0.5,charsize=1.,orientation=angle[i]
   endfor

return
end 

hockeypuckplot
end

