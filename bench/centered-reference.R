library(metafor)
code<-readLines('corpus.R');eval(parse(text=code[seq_len(grep('^datasets<-',code)-1)]))
corpus<-readRDS('corpus.rds'); ids<-readLines('diagnostic-ids.txt')
out<-file('centered-reference.jsonl','w')
for(c in corpus)if(c[["id", exact=TRUE]]%in%ids){
 d<-c[["rows", exact=TRUE]];mx<-mean(d[["x", exact=TRUE]]);sx<-sd(d[["x", exact=TRUE]]);d[["z", exact=TRUE]]<-(d[["x", exact=TRUE]]-mx)/sx
 result<-tryCatch({
  f<-rma(yi,vi,mods=~z,data=d,method='PM',test='adhoc',control=list(tol=1e-15,threshold=1e-15,maxiter=1000))
  A<-matrix(c(1,0,-mx/sx,1/sx),2);b<-as.numeric(A%*%f[["beta", exact=TRUE]]);V<-A%*%vcov(f)%*%t(A);se<-sqrt(diag(V));crit<-qt(.975,f[["ddf", exact=TRUE]])
  pred<-predict(f,newmods=0)
  list(beta=b,se=se,ci_lb=b-crit*se,ci_ub=b+crit*se,tau2=f[["tau2", exact=TRUE]],R2=f[["R2", exact=TRUE]]/100,QE=f[["QE", exact=TRUE]],QE_p=f[["QEp", exact=TRUE]],q=f[["s2w", exact=TRUE]],pred=pred[["pred", exact=TRUE]],pred_se=pred[["se", exact=TRUE]],pi_lb=pred[["pi.lb", exact=TRUE]],pi_ub=pred[["pi.ub", exact=TRUE]],slope_t=b[2]/se[2])
 },error=function(e)list(error=conditionMessage(e)))
 writeLines(js(list(id=c[["id", exact=TRUE]],main=result)),out)
}
close(out);cat(length(ids),'centered-reference diagnostics recorded\n')
