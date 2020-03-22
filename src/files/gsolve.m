% from http://www.pauldebevec.com/Research/HDR/debevec-siggraph97.pdf
function [g] = gsolve(Z,B,l,w,index) 
%disp(Z);

n = 256;
A = zeros(size(Z,1)*size(Z,2)+n+1,n+size(Z,1)); 
b = zeros(size(A,1),1);

k = 1;
for i=1:size(Z,1)
	for j=1:size(Z,2)
		wij = w(Z(i,j)+1);
		A(k,Z(i,j)+1) = wij; 
		A(k,n+i) = -wij; 
		b(k,1) = wij * B(j);
        k=k+1;
    end 
end

A(k,129) = 1;
k=k+1;

for i=1:n-2
	A(k,i)=l*w(i+1);
    A(k,i+1)=-2*l*w(i+1);
    A(k,i+2)=l*w(i+1);
    k=k+1;
end
disp(nnz(A));
%fname = sprintf('matlab_A_%d.mat',index);
%save(fname, A)
%fnameb = sprintf('matlab_b_%d.mat',index);
%save(fnameb, b)
save(['matlab_a ',num2str(index),'.mat'],'A');
save(['matlab_b ',num2str(index),'.mat'],'b');

x = A\b;

save(['matlab_x ',num2str(index),'.mat'],'x');


g = x(1:n);
%lE = x(n+1:size(x,1));