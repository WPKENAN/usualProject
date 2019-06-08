clc
X=zeros(n,2);
for i=1:n
    X(i,:)=[S(i).xd,S(i).yd];
end
figure;
plot(X(:,1),X(:,2),'.');
title 'Randomly Generated Data';

opts = statset('Display','final');
[idx,C] = kmeans(X,4,'Distance','cityblock',...
    'Replicates',5,'Options',opts);

figure;
plot(X(idx==1,1),X(idx==1,2),'r.','MarkerSize',12)
hold on
plot(X(idx==2,1),X(idx==2,2),'b.','MarkerSize',12)
hold on
plot(X(idx==3,1),X(idx==3,2),'g.','MarkerSize',12)
hold on
plot(X(idx==4,1),X(idx==4,2),'y.','MarkerSize',12)
hold on
for i=1:n
    text(X(i,1),X(i,2),num2str(i));
end
plot(C(:,1),C(:,2),'kx',...
     'MarkerSize',15,'LineWidth',3) 
legend('Cluster 1','Cluster 2','Cluster 3','Centroids',...
       'Location','NW')
title 'Cluster Assignments and Centroids'
hold off