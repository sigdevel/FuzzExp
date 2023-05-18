%%%This code perform statistical analysis of the networks simulated with
%%%all possible 2 nodes combinations. Goal: identifying non-monotonic
%%%behaviors

clear all
close all
clc

%This code loops over the Network datasets already simulated
SET={'Two','Three','Four'};
Nset=[2 3 4];

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%Uncomment these lines to run the Tol search%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% %This is the tolerance interval that we will examine
% Tol=(1.01:0.01:2);
% figure
% for j=1:length(SET)
% 
%     %Simulation Data Loading
%     load([SET{j},'NodeNetworkSimulation'])
%     %Sensor types
%     SensType=(1:6);
%     for i=1:length(Tol) 
%         %Detecting the nonmonotonic behaviors divided by sensor type
%         for k=1:length(SensType)
%             [~,Interesting(i,(j-1)*6+k)]=MonotonicAnalysisNodeNetworks(eval(['Y',num2str(SensType(k))]),Yindex,Tol(i),Nset(j));
%         end
%     end
%     subplot(1,length(SET),j)
%     plot(Tol,Interesting(:,(j-1)*6+1:j*6))
%     
% end
% 
% 
Tol=1.21; %I picked this tolerance based on the grid that I designed above

%Identifying the solutions that use only 1 input (Time series)
for j=1:length(SET)    
    %Simulation Data Loading
    load([SET{j},'NodeNetworkSimulation'])
    %Sensor types
    SensType=(1:6);
    %Detecting the nonmonotonic behaviors divided by sensor type
    for k=1:length(SensType)
        %Identifying useful solutions
        [InterestingNet{j,k},~,InterestingInputs{j,k},InterestingNetF{j,k},InterestingSeries{j,k},InterestingSeriesF{j,k}]=MonotonicAnalysisNodeNetworks(eval(['Y',num2str(SensType(k))]),Yindex,Tol,Nset(j));
    end
end

save('NonMonotonicNetworks','InterestingNet','InterestingInputs','InterestingNetF','InterestingSeries','InterestingSeriesF')

cont=0;
for i=1:size(InterestingSeriesF,2)
    for j=1:size(InterestingSeriesF,1)
        cont=cont+1;
        subplot(6,3,cont)
        plot(InterestingSeriesF{j,i}')
    end
end

set(gca,'FontSize',15)
ylabel('Fluorescence');
xlabel('Time (hr)');  

%Now it selects the most interesting behaviors for each Node-network and
%each sensor
for j=1:size(InterestingNetF,2)
    for i=1:size(InterestingNetF,1)
        if isempty(InterestingNetF{i,j})
            M(i,j)=0;
            MaxInterestingNetF{i,j}=[];
        else
            [M(i,j),Ind]=max(InterestingNetF{i,j}(:,3));
            MaxInterestingNetF{i,j}=InterestingNetF{i,j}(Ind,:);
        end
    end
end
%The optimization happens at the end of the code


%Then, it analyzes the steady-state values for variable beta, fixed IAA and
%alpha
for j=1:length(SET)
    
    load([SET{j},'NodeNetworkSimulationFixedWithMISO'])
    %Sensor types
    SensType=(1:6);
    for k=1:length(SensType)
        [InterestingNetSSB{j,k},~,InterestingInputsSSB{j,k},InterestingNetSSFB{j,k},InterestingSeriesSSB{j,k},InterestingSeriesSSFB{j,k}]=MonotonicAnalysisNodeNetworks(eval(['Y',num2str(SensType(k)), 'SS']),YSSindex,Tol,Nset(j));
    end
    %Then, it analyzes the steady-state values for variable alpha, fixed beta and
    %IAA
    beta=[0 1 5 10 100];
    IAA=[0 100 500 1000 5000];
    alpha=[0 1 5 10 50 200 1000];
    %Adjusting the index matrix shape
    YindexA=unique(YSSindex(:,1:Nset(j)),'rows');
    YIAA=kron(ones(length(YindexA)*length(beta),1),IAA');

    Ybeta=kron(beta', ones(length(IAA),1));
    Ybeta=repmat(Ybeta,length(YindexA));
    Ybeta=Ybeta(:,1);

    YA=kron(YindexA, ones(length(IAA)*length(beta),1));

    YSSindexA=[YA Ybeta YIAA];

    %Adjusting the data matrix shape
    Y1SSA=[];
    for i=1:size(YindexA,1)
        Y1SSAt=reshape(Y1SS(1+(i-1)*length(IAA)*length(alpha):i*length(IAA)*length(alpha),:),length(alpha),length(IAA)*length(beta))';
        Y2SSAt=reshape(Y2SS(1+(i-1)*length(IAA)*length(alpha):i*length(IAA)*length(alpha),:),length(alpha),length(IAA)*length(beta))';
        Y3SSAt=reshape(Y3SS(1+(i-1)*length(IAA)*length(alpha):i*length(IAA)*length(alpha),:),length(alpha),length(IAA)*length(beta))';
        Y4SSAt=reshape(Y4SS(1+(i-1)*length(IAA)*length(alpha):i*length(IAA)*length(alpha),:),length(alpha),length(IAA)*length(beta))';
        Y5SSAt=reshape(Y5SS(1+(i-1)*length(IAA)*length(alpha):i*length(IAA)*length(alpha),:),length(alpha),length(IAA)*length(beta))';
        Y6SSAt=reshape(Y6SS(1+(i-1)*length(IAA)*length(alpha):i*length(IAA)*length(alpha),:),length(alpha),length(IAA)*length(beta))';
        if i==1
            Y1SSA=Y1SSAt;
            Y2SSA=Y2SSAt;
            Y3SSA=Y3SSAt;
            Y4SSA=Y4SSAt;
            Y5SSA=Y5SSAt;
            Y6SSA=Y6SSAt;
        else
            Y1SSA=[Y1SSA;Y1SSAt];
            Y2SSA=[Y2SSA;Y2SSAt];
            Y3SSA=[Y3SSA;Y3SSAt];
            Y4SSA=[Y4SSA;Y4SSAt];
            Y5SSA=[Y5SSA;Y5SSAt];
            Y6SSA=[Y6SSA;Y6SSAt];
        end
    end
    %Computing the non-monotonic search
    for k=1:length(SensType)
        [InterestingNetSSA{j,k},~,InterestingInputsSSA{j,k},InterestingNetSSFA{j,k},InterestingSeriesSSA{j,k},InterestingSeriesSSFA{j,k}]=MonotonicAnalysisNodeNetworks(eval(['Y',num2str(SensType(k)), 'SSA']),YSSindexA,Tol,Nset(j));
    end

    %Then, it analyzes the steady-state values for variable IAA, fixed beta and
    %alpha
    %Adjusting the index matrix shape
    YindexI=unique(YSSindexA(:,1:Nset(j)),'rows');
    Ybeta=kron(ones(length(YindexI)*length(alpha),1),beta');

    Yalpha=kron(alpha', ones(length(beta),1));
    Yalpha=repmat(Yalpha,length(YindexI));
    Yalpha=Yalpha(:,1);

    YI=kron(YindexI, ones(length(alpha)*length(beta),1));

    YSSindexI=[YI Yalpha Ybeta];

    %Adjusting the data matrix shape
    for i=1:size(YindexI,1)
        Y1SSIt=reshape(Y1SSA(1+(i-1)*length(IAA)*length(beta):i*length(IAA)*length(beta),:),length(IAA),length(alpha)*length(beta))';
        Y2SSIt=reshape(Y2SSA(1+(i-1)*length(IAA)*length(beta):i*length(IAA)*length(beta),:),length(IAA),length(alpha)*length(beta))';
        Y3SSIt=reshape(Y3SSA(1+(i-1)*length(IAA)*length(beta):i*length(IAA)*length(beta),:),length(IAA),length(alpha)*length(beta))';
        Y4SSIt=reshape(Y4SSA(1+(i-1)*length(IAA)*length(beta):i*length(IAA)*length(beta),:),length(IAA),length(alpha)*length(beta))';
        Y5SSIt=reshape(Y5SSA(1+(i-1)*length(IAA)*length(beta):i*length(IAA)*length(beta),:),length(IAA),length(alpha)*length(beta))';
        Y6SSIt=reshape(Y6SSA(1+(i-1)*length(IAA)*length(beta):i*length(IAA)*length(beta),:),length(IAA),length(alpha)*length(beta))';
        if i==1
            Y1SSI=Y1SSIt;
            Y2SSI=Y2SSIt;
            Y3SSI=Y3SSIt;
            Y4SSI=Y4SSIt;
            Y5SSI=Y5SSIt;
            Y6SSI=Y6SSIt;
        else
            Y1SSI=[Y1SSI;Y1SSIt];
            Y2SSI=[Y2SSI;Y2SSIt];
            Y3SSI=[Y3SSI;Y3SSIt];
            Y4SSI=[Y4SSI;Y4SSIt];
            Y5SSI=[Y5SSI;Y5SSIt];
            Y6SSI=[Y6SSI;Y6SSIt];
        end
    end
    %Computing the non-monotonic search
    for k=1:length(SensType)
        [InterestingNetSSI{j,k},~,InterestingInputsSSI{j,k},InterestingNetSSFI{j,k},InterestingSeriesSSI{j,k},InterestingSeriesSSFI{j,k}]=MonotonicAnalysisNodeNetworks(eval(['Y',num2str(SensType(k)), 'SSI']),YSSindexI,Tol,Nset(j));
    end   

end

filename='NonMonotonicNetworksSS';
save(filename,'InterestingNetSSB','InterestingSeriesSSB','InterestingNetSSA','InterestingSeriesSSA','InterestingNetSSI','InterestingSeriesSSI')
    
figure
cont=0;
for i=1:size(InterestingSeriesSSB,2)
    for j=1:size(InterestingSeriesSSB,1)
        cont=cont+1;
        subplot(6,3,cont)
        plot(InterestingSeriesSSB{j,i}')
    end
end

set(gca,'FontSize',15)
ylabel('Fluorescence');
xlabel('Time (hr)');

figure
cont=0;
for i=1:size(InterestingSeriesSSA,2)
    for j=1:size(InterestingSeriesSSA,1)
        cont=cont+1;
        subplot(6,3,cont)
        plot(InterestingSeriesSSA{j,i}')
    end
end

set(gca,'FontSize',15)
ylabel('Fluorescence');
xlabel('Time (hr)');

figure
cont=0;
for i=1:size(InterestingSeriesSSI,2)
    for j=1:size(InterestingSeriesSSI,1)
        cont=cont+1;
        subplot(6,3,cont)
        plot(InterestingSeriesSSI{j,i}')
    end
end

set(gca,'FontSize',15)
ylabel('Fluorescence');
xlabel('Time (hr)');

%Now it selects the most interesting behaviors for each Node-network and
%each sensor
%First the SSA combo
for j=1:size(InterestingNetSSA,2)
    for i=1:size(InterestingNetSSA,1)
        if isempty(InterestingNetSSA{i,j})
            MSSA(i,j)=0;
            MaxInterestingNetSSA{i,j}=[];
        else
            [MSSA(i,j),Ind]=max(InterestingNetSSA{i,j}(:,3));
            MaxInterestingNetSSA{i,j}=InterestingNetSSA{i,j}(Ind,:);
            Temp=InterestingInputsSSA{i,j}(Ind);
            [M,I]=max(Temp{1}(:,1));
            MaxInterestingNetSSAInput{i,j}=Temp{1}(I,end:-1:2);
        end
    end
end
%Then the SSB combo
for j=1:size(InterestingNetSSB,2)
    for i=1:size(InterestingNetSSB,1)
        if isempty(InterestingNetSSB{i,j})
            MSSB(i,j)=0;
            MaxInterestingNetSSB{i,j}=[];
        else
            [MSSB(i,j),Ind]=max(InterestingNetSSB{i,j}(:,3));
            MaxInterestingNetSSB{i,j}=InterestingNetSSB{i,j}(Ind,:);
            Temp=InterestingInputsSSB{i,j}(Ind);
            [M,I]=max(Temp{1}(:,1));
            MaxInterestingNetSSBInput{i,j}=Temp{1}(I,2:end);
        end
    end
end
%And finally the SSI combo
for j=1:size(InterestingNetSSI,2)
    for i=1:size(InterestingNetSSI,1)
        if isempty(InterestingNetSSI{i,j})
            MSSI(i,j)=0;
            MaxInterestingNetSSI{i,j}=[];
        else
            [MSSI(i,j),Ind]=max(InterestingNetSSI{i,j}(:,3));
            MaxInterestingNetSSI{i,j}=InterestingNetSSI{i,j}(Ind,:);
            Temp=InterestingInputsSSI{i,j}(Ind);
            [M,I]=max(Temp{1}(:,1));
            MaxInterestingNetSSIInput{i,j}=Temp{1}(I,2:end);
        end
    end
end

%The final step of the code: compute the optimization of each network
for j=1:size(MaxInterestingNetF,2)
    for i=1:size(MaxInterestingNetF,1)
        if isempty(MaxInterestingNetF{i,j})
            OptInterestingNetF{i,j}=[];
        else
            [OptInterestingNetF{i,j},OldSym{i,j},NewSym{i,j}]=OptimalNonMonoTS(MaxInterestingNetF{i,j},j,Nset(i));
        end
    end
end
%INPUT={'alpha','IAA',''beta'}; input order
for j=1:size(MaxInterestingNetSSA,2)
    for i=1:size(MaxInterestingNetSSA,1)
        if isempty(MaxInterestingNetSSA{i,j})
            OptInterestingNetSSA{i,j}=[];
        else
            [OptInterestingNetSSA{i,j},OldSymSSA{i,j},NewSymSSA{i,j}]=OptimalNonMonoSS(MaxInterestingNetSSA{i,j},j,Nset(i),1,MaxInterestingNetSSAInput{i,j});
        end
    end
end

for j=1:size(MaxInterestingNetSSB,2)
    for i=1:size(MaxInterestingNetSSB,1)
        if isempty(MaxInterestingNetSSB{i,j})
            OptInterestingNetSSB{i,j}=[];
        else
            [OptInterestingNetSSB{i,j},OldSymSSB{i,j},NewSymSSB{i,j}]=OptimalNonMonoSS(MaxInterestingNetSSB{i,j},j,Nset(i),3,MaxInterestingNetSSBInput{i,j});
        end
    end
end

for j=1:size(MaxInterestingNetSSI,2)
    for i=1:size(MaxInterestingNetSSI,1)
        if isempty(MaxInterestingNetSSI{i,j})
            OptInterestingNetSSI{i,j}=[];
        else
            [OptInterestingNetSSI{i,j},OldSymSSI{i,j},NewSymSSI{i,j}]=OptimalNonMonoSS(MaxInterestingNetSSI{i,j},j,Nset(i),2,MaxInterestingNetSSIInput{i,j});
        end
    end
end

save('OptimalNonMonotonic','OptInterestingNetSSB','OptInterestingNetSSA','OptInterestingNetSSI','OptInterestingNetF','OldSymSSI','NewSymSSI','OldSymSSB','NewSymSSB','OldSymSSA','NewSymSSA','OldSym','NewSym','MaxInterestingNetF','MaxInterestingNetSSA','MaxInterestingNetSSB','MaxInterestingNetSSI','M','MSSA','MSSI','MSSB')