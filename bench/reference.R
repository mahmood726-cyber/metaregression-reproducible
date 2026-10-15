library(metafor)
code<-readLines('corpus.R'); eval(parse(text=code[seq_len(grep('^datasets<-',code)-1)]))
corpus<-readRDS('corpus.rds')
writej(list(R=R.version.string,metafor=as.character(packageVersion('metafor')),metadat=as.character(packageVersion('metadat')),test='adhoc',method='PM',pm_control=list(threshold=1e-12,tol=1e-12,maxiter=1000)),'versions.json')
outfile<-if(length(commandArgs(TRUE)))commandArgs(TRUE)[1] else 'reference.jsonl'
done<-if(file.exists(outfile))sub('^\\{"id":"([^"]+)".*','\\1',readLines(outfile))else character()
out<-file(outfile,'a'); on.exit(close(out))
for(i in seq_along(corpus)) {
 c<-corpus[[i]];d<-c[["rows", exact=TRUE]]; warnings<-character()
 if(c[["id", exact=TRUE]]%in%done)next
 attempt<-function(expr)withCallingHandlers(tryCatch(expr,error=function(e)list(error=conditionMessage(e))),warning=function(w){warnings<<-c(warnings,conditionMessage(w));invokeRestart('muffleWarning')})
 f<-attempt(rma(yi,vi,mods=~x,data=d,method='PM',test='adhoc',control=list(threshold=1e-12,tol=1e-12,maxiter=1000)))
 r<-list(id=c[["id", exact=TRUE]],k=nrow(d))
 if(inherits(f,'rma')) {
  p<-predict(f,newmods=mean(d[["x", exact=TRUE]])); xb<-range(d[["x", exact=TRUE]]);xb<-xb+c(-1,1)*diff(xb)*.08
  bp<-predict(f,newmods=seq(xb[1],xb[2],length.out=201))
  r[["main", exact=TRUE]]<-list(beta=as.numeric(f[["beta", exact=TRUE]]),se=f[["se", exact=TRUE]],t=f[["zval", exact=TRUE]],p=f[["pval", exact=TRUE]],ci_lb=f[["ci.lb", exact=TRUE]],ci_ub=f[["ci.ub", exact=TRUE]],tau2=f[["tau2", exact=TRUE]],I2=f[["I2", exact=TRUE]],H2=f[["H2", exact=TRUE]],R2=f[["R2", exact=TRUE]]/100,QM=f[["QM", exact=TRUE]],QM_p=f[["QMp", exact=TRUE]],QE=f[["QE", exact=TRUE]],QE_p=f[["QEp", exact=TRUE]],q=f[["s2w", exact=TRUE]],df=f[["ddf", exact=TRUE]],pred=p[["pred", exact=TRUE]],pred_se=p[["se", exact=TRUE]],pi_lb=p[["pi.lb", exact=TRUE]],pi_ub=p[["pi.ub", exact=TRUE]],band=list(x=seq(xb[1],xb[2],length.out=201),pred=bp[["pred", exact=TRUE]],lo=bp[["ci.lb", exact=TRUE]],hi=bp[["ci.ub", exact=TRUE]]))
  r[["knha", exact=TRUE]]<-attempt({g<-rma(yi,vi,mods=~x,data=d,method='PM',test='knha',control=list(threshold=1e-12,tol=1e-12,maxiter=1000));list(se=g[["se", exact=TRUE]],ci_lb=g[["ci.lb", exact=TRUE]],ci_ub=g[["ci.ub", exact=TRUE]])})
 }else r[["main", exact=TRUE]]<-f
 r[["permutation", exact=TRUE]]<-list(status=if(nrow(d)<4)'not offered for k<4' else if(nrow(d)>7)'not comparable: app LCG and R RNG differ' else 'pending exact run')
 r[["ls", exact=TRUE]]<-if(nrow(d)<4)list(status='not offered for k<4') else attempt({
  setTimeLimit(elapsed=60,transient=TRUE)
  l<-tryCatch(rma(yi,vi,mods=~x,scale=~x,data=d,method='ML',test='z',control=list(maxiter=10000)),finally=setTimeLimit(cpu=Inf,elapsed=Inf,transient=FALSE))
  list(beta=as.numeric(l[["beta", exact=TRUE]]),betaSE=l[["se", exact=TRUE]],alpha=as.numeric(l[["alpha", exact=TRUE]]),alphaSE=l[["se.alpha", exact=TRUE]],alpha_p=l[["pval.alpha", exact=TRUE]],tau2=l[["tau2", exact=TRUE]],logLik=as.numeric(logLik(l)),beta_lb=l[["ci.lb", exact=TRUE]],beta_ub=l[["ci.ub", exact=TRUE]])
 })
 r[["warnings", exact=TRUE]]<-warnings;writeLines(js(r),out,useBytes=TRUE);flush(out)
 if(i%%25==0)cat(i,'/',length(corpus),'references\n')
}
close(out)
cat(length(corpus),'reference configurations recorded\n')
