library(metafor)
code<-readLines('corpus.R');eval(parse(text=code[seq_len(grep('^datasets<-',code)-1)]))
corpus<-readRDS('corpus.rds');corpus<-Filter(function(c)c[["k", exact=TRUE]]>=4&&c[["k", exact=TRUE]]<=7,corpus)
outfile<-if(length(commandArgs(TRUE)))commandArgs(TRUE)[1] else 'permutation-reference.jsonl'
done<-if(file.exists(outfile))sub('^\\{"id":"([^"]+)".*','\\1',readLines(outfile))else character()
args<-commandArgs(TRUE)
if(length(args)>=3){
 basefile<-'permutation-reference.jsonl'
 if(file.exists(basefile))done<-unique(c(done,sub('^\\{"id":"([^"]+)".*','\\1',readLines(basefile))))
 corpus<-corpus[(seq_along(corpus)-1)%%as.integer(args[3])==as.integer(args[2])]
}
out<-file(outfile,'a')
for(i in seq_along(corpus)){
 c<-corpus[[i]];d<-c[["rows", exact=TRUE]];warnings<-character()
 if(c[["id", exact=TRUE]]%in%done)next
 p<-withCallingHandlers(tryCatch({
  f<-rma(yi,vi,mods=~x,data=d,method='PM',test='adhoc',control=list(threshold=1e-12,tol=1e-12,maxiter=1000))
  z<-permutest(f,exact=TRUE,progbar=FALSE)
  list(p=as.numeric(z[["pval", exact=TRUE]][2]),QM_p=z[["QMp", exact=TRUE]],exact=z[["exact", exact=TRUE]],iter=z[["iter", exact=TRUE]])
 },error=function(e)list(error=conditionMessage(e))),warning=function(w){warnings<<-c(warnings,conditionMessage(w));invokeRestart('muffleWarning')})
 writeLines(js(list(id=c[["id", exact=TRUE]],result=p,warnings=warnings)),out);flush(out)
 cat(i,'/',length(corpus),'exact permutation references\n')
}
close(out);cat(length(corpus),'exact permutation configurations recorded\n')
