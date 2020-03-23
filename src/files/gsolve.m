% from http://www.pauldebevec.com/Research/HDR/debevec-siggraph97.pdf
function [g,lE] = gsolve(Z,B,l,w) 
disp(Z);
%exit(0);
n = 256;
A = zeros(size(Z,1)*size(Z,2)+n+1,n+size(Z,1)); 
b = zeros(size(A,1),1);
%% Include the data−fitting equations
disp(size(Z,1) +","+ size(Z,2)+","+n+","+1+",," + n+","+size(Z,1));
disp("" + size(Z))
disp("" + size(A))
disp("" + size(b))
k = 1;
for i=1:size(Z,1)
	for j=1:size(Z,2)
		wij = w(Z(i,j)+1);
		A(k,Z(i,j)+1) = wij; 
		A(k,n+i) = -wij; 
        disp(i +","+ j);
		b(k,1) = wij * B(j);
        k=k+1;
	end 
end
disp(b);

A(k,129) = 1;
k=k+1;

for i=1:n-2
	A(k,i)=l*w(i+1); A(k,i+1)=-2*l*w(i+1); A(k,i+2)=l*w(i+1); k=k+1;
end

x = A\b;

g = x(1:n);
lE = x(n+1:size(x,1));