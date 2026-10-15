library(metafor); library(metadat); library(meta)
options(warn=1)
# Full precision JSON without an additional package dependency.
js <- function(x) {
 if(is.null(x)) return('null')
 if(is.data.frame(x)) return(js(lapply(seq_len(nrow(x)),function(i) as.list(x[i,,drop=FALSE]))))
 if(is.list(x)) {v<-vapply(x,js,''); if(!is.null(names(x))) return(paste0('{',paste(paste0(vapply(names(x),js,''),':',v),collapse=','),'}')); return(paste0('[',paste(v,collapse=','),']'))}
 if(length(x)!=1) return(paste0('[',paste(vapply(as.list(x),js,''),collapse=','),']'))
 if(is.na(x)|| (is.numeric(x)&&!is.finite(x))) return('null')
 if(is.logical(x)) return(if(x)'true' else 'false')
 if(is.numeric(x)) return(sprintf('%.17g',x))
 encodeString(as.character(x),quote='"')
}
writej<-function(x,f) writeLines(js(x),f,useBytes=TRUE)
datasets<-data(package='metadat')[["results", exact=TRUE]][,'Item']; corpus<-list(); audit<-list(); recipes<-list(); exclusions<-list()
idfields<-c('id','study','trial','esid','studyid','study_id','sampleid','sample','obs','article','experiment','district','school','person','team')
source('supplemental.R')
for(n in datasets) {
 e<-new.env(parent=globalenv()); data(list=n,package='metadat',envir=e)
 seen<-character(); count0<-length(corpus); seqno<-0
 capture<-function(d, origin) {
  if(is.data.frame(d)&&all(c('TE','seTE')%in%names(d))) {d[["yi", exact=TRUE]]<-d[["TE", exact=TRUE]];d[["vi", exact=TRUE]]<-d[["seTE", exact=TRUE]]^2}
  if(!is.data.frame(d)||!all(c('yi','vi')%in%names(d))) return()
  for(col in names(d)) if(is.character(d[[col]]) || is.factor(d[[col]])) {
   text<-trimws(as.character(d[[col]]));nz<-!is.na(text)&nzchar(text)
   if(any(nz)&&all(grepl('^[+-]?[0-9]*\\.?[0-9]+([eE][+-]?[0-9]+)?$',text[nz]))) d[[col]]<-suppressWarnings(as.numeric(text))
  }
  key<-paste(sprintf('%.17g',d[["yi", exact=TRUE]]),sprintf('%.17g',d[["vi", exact=TRUE]]),collapse='|')
  if(key%in%seen) return(); seen<<-c(seen,key); seqno<<-seqno+1
  effect<-paste0(n,'/e',seqno); recipes[[effect]]<<-origin
  for(m in setdiff(names(d),c('yi','vi','sei'))) {
   reason<-NULL
   if(!is.numeric(d[[m]])) reason<-'non-numeric: page has no factor encoding'
   else if(tolower(m)%in%idfields || grepl('(^|[._])(id|ID)$',m)) reason<-'identifier, not a study characteristic'
   else if(grepl('^(yi|vi|sei|v[12]i)$',m)) reason<-'effect/variance output'
   ok<-if(is.numeric(d[[m]])) is.finite(d[["yi", exact=TRUE]])&is.finite(d[["vi", exact=TRUE]])&d[["vi", exact=TRUE]]>0&is.finite(d[[m]]) else rep(FALSE,nrow(d))
   if(is.null(reason)&&sum(ok)<3) reason<-'fewer than 3 complete rows with positive variance'
   if(is.null(reason)&&length(unique(d[[m]][ok]))<2) reason<-'constant moderator'
   if(!is.null(reason)) {exclusions[[length(exclusions)+1]]<<-list(effect=effect,moderator=m,reason=reason); next}
   rows<-data.frame(study=paste0(n,':',which(ok)),yi=d[["yi", exact=TRUE]][ok],vi=d[["vi", exact=TRUE]][ok],x=d[[m]][ok])
   corpus[[length(corpus)+1]]<<-list(id=paste0(effect,'/',m),dataset=n,effect=effect,moderator=m,k=nrow(rows),rows=rows)
  }
 }
 walk<-function(x,label) {if(is.data.frame(x)) capture(x,label) else if(is.list(x)) for(nm in names(x)) if(is.data.frame(x[[nm]])) capture(x[[nm]],paste0(label,'$',nm))}
 walk(e[[n]],'precomputed yi/vi supplied by metadat')
 ep<-file.path('docs',paste0(n,'.R'))
 ex<-if(file.exists(ep))sub('^##D ?', '',readLines(ep,warn=FALSE)) else character()
 exprs<-tryCatch(parse(text=ex),error=function(er)expression())
 logs<-list()
 for(expr in exprs) {
  # Execute data preparation only; never model/plot/network/package-install examples.
  calls<-all.names(expr,functions=TRUE)
  if(!is.call(expr)) next
  modelcall<-if(as.character(expr[[1]])%in%c('<-','='))expr[[3]] else expr
  if(is.call(modelcall)&&is.symbol(modelcall[[1]])&&as.character(modelcall[[1]])%in%c('rma','rma.uni','rma.mh','rma.peto','rma.mv')) {
   args<-as.list(modelcall)[-1]; an<-names(args); if(is.null(an))an<-rep('',length(args))
   pos<-which(an==''); if(length(pos))an[pos]<-c('yi','vi')[seq_along(pos)];names(args)<-an
   args<-args[intersect(names(args),names(formals(escalc)))]; if(is.null(args[["measure", exact=TRUE]]))args[["measure", exact=TRUE]]<-'GEN'
   ec<-as.call(c(list(as.name('escalc')),args))
   val<-tryCatch(eval(ec,e),error=function(er)NULL)
   if(!is.null(val)) capture(val,paste('documented model inputs:',paste(deparse(ec),collapse=' ')))
  }
  if(!as.character(expr[[1]])%in%c('<-','='))next
  if(any(grepl('^(rma|lm$|glm|gam|stan|jags|bayesmeta|forest|plot|predict|confint|profile|anova|permutest|aggregate.escalc|optim|download|source|system|install|library|require)',calls))) next
  before<-ls(e)
  er<-tryCatch({eval(expr,e);NULL},error=function(er)conditionMessage(er))
  origin<-paste(deparse(expr,width.cutoff=500),collapse=' ')
  logs[[length(logs)+1]]<-list(code=origin,error=er)
  if(is.null(er)) for(nm in ls(e)) {v<-e[[nm]]; if(is.data.frame(v)) capture(v,origin)}
 }
 supplement(e[[n]],n,capture)
 if(is.list(e[[n]])&&!is.data.frame(e[[n]])) for(part in names(e[[n]])) if(is.data.frame(e[[n]][[part]])) supplement(e[[n]][[part]],paste0(n,'$',part),capture)
 audit[[n]]<-list(dataset=n,configurations=length(corpus)-count0,effects=seqno,status=if(length(corpus)>count0)'used' else 'excluded: no numeric moderator with supported effect and >=3 complete rows',preparation=logs)
 cat(n,':',length(corpus)-count0,'configurations\n')
}
writej(corpus,'corpus.json'); writej(audit,'dataset-audit.json'); writej(recipes,'effect-recipes.json');writej(exclusions,'moderator-exclusions.json')
saveRDS(corpus,'corpus.rds')
cat(length(corpus),'configurations;',sum(vapply(audit,function(x)x[["configurations", exact=TRUE]]>0,TRUE)),'/',length(datasets),'datasets used\n')
