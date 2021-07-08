; The 2MASS Redshift Survey
; Huchra et al., ApJS, in press
;
; http://tdc-www.harvard.edu/2mrs/
; catalog version 2.4, 2011 Dec 16
; maintained by Lucas Macri, lmacri@tamu.edu
;
; This routine will read all of the ASCII catalog contents into a structure
; called "g" with "ng" items

pro tmrs

a={id:'',r:0.,d:0.,l:0.,b:0.,k:0.,h:0.,j:0.,kt:0.,ht:0.,jt:0.,ek:0.,eh:0.,ej:0.,ekt:0.,eht:0.,ejt:0.,ebv:0.,ri:0.,rt:0.,ba:0.,cf:'',t:'',ts:'',v:0l,ev:0,vc:'',vsrc:'',catid:''}
frm='(A16,4(F10.5),6(F7.3),10(F6.3),1x,A4,1x,A5,1x,A2,I7,I4,1x,A1,1x,A19,1x,A28,X)'

g=replicate(a,45000)
ng=0l
line=''
openr,lun,'2mrs_1175_done.dat',/get_lun
for j=0l,9 do $
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
stop

return
end
