# Fresh fits for one configuration; primary failures propagate to the caller.
refit_worker <- function(c) {
  field<-function(x,k){if(!is.list(x)||!(k%in%names(x)))stop('Missing field: ',k);x[[k,exact=TRUE]]}
  columns<-lapply(c('yi','vi','x'),function(q)vapply(field(c,'rows'),function(r){v<-field(r,q);if(!is.numeric(v)||length(v)!=1||!is.finite(v))stop('Invalid corpus number');v},0))
  d<-setNames(as.data.frame(columns),c('yi','vi','x'));k<-nrow(d)
  if(k!=field(c,'k')||k<3||any(d[['vi',exact=TRUE]]<=0)||length(unique(d[['x',exact=TRUE]]))<2)stop('Corpus shape')
  f<-metafor::rma(yi,vi,mods=~x,data=d,method='PM',test='adhoc',control=list(tol=1e-12,threshold=1e-12,maxiter=1000))
  p<-predict(f,newmods=mean(d[['x',exact=TRUE]]));xb<-range(d[['x',exact=TRUE]]);xb<-xb+c(-1,1)*diff(xb)*.08
  bp<-predict(f,newmods=seq(xb[1],xb[2],length.out=201))
  rr<-list(beta=as.numeric(field(f,'beta')),se=field(f,'se'),ci_lb=field(f,'ci.lb'),ci_ub=field(f,'ci.ub'),tau2=field(f,'tau2'),R2=field(f,'R2')/100,QE=field(f,'QE'),QE_p=field(f,'QEp'),q=field(f,'s2w'),df=field(f,'ddf'),pred=field(p,'pred'),pred_se=field(p,'se'),pi_lb=field(p,'pi.lb'),pi_ub=field(p,'pi.ub'))
  perm<-if(k>=4&&k<=7)metafor::permutest(f,exact=TRUE,progbar=FALSE) else NULL
  ls<-if(k<4)list(status='not offered for k<4') else tryCatch({
    setTimeLimit(elapsed=60,transient=TRUE)
    l<-tryCatch(metafor::rma(yi,vi,mods=~x,scale=~x,data=d,method='ML',test='z',control=list(maxiter=10000)),finally=setTimeLimit(cpu=Inf,elapsed=Inf,transient=FALSE))
    list(beta=as.numeric(field(l,'beta')),betaSE=field(l,'se'),alpha=as.numeric(field(l,'alpha')),alphaSE=field(l,'se.alpha'),alpha_p=field(l,'pval.alpha'),tau2=field(l,'tau2'),logLik=as.numeric(logLik(l)),beta_lb=field(l,'ci.lb'),beta_ub=field(l,'ci.ub'))
  },error=function(e)list(error=conditionMessage(e)))
  cat('Fresh fit complete: ',field(c,'id'),'\n',sep='');flush.console()
  list(id=field(c,'id'),main=rr,t=field(f,'zval'),p=field(f,'pval'),band=list(pred=field(bp,'pred'),lo=field(bp,'ci.lb'),hi=field(bp,'ci.ub')),permutation=if(is.null(perm))NULL else list(p=as.numeric(field(perm,'pval')[2])),ls=ls)
}
