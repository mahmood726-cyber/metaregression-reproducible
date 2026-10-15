# Final source-level audit: exclude an intermediate transform, an altered-example
# outcome, identifiers, and duplicate effective configurations. Keep raw journals.
library(metafor)
code<-readLines('corpus.R');eval(parse(text=code[seq_len(grep('^datasets<-',code)-1)]))
corpus<-readRDS('corpus.rds');kept<-list();excluded<-list();seen<-list()
for(c in corpus){
 reason<-NULL
 if(c[["effect", exact=TRUE]]=='dat.obrien2003/e3')reason<-'intermediate percent transform: yi multiplied by 100 before vi multiplied by 100^2; not a valid final definition'
 if(c[["effect", exact=TRUE]]=='dat.dorn2007/e2')reason<-'documentation replaces one observed log risk ratio with a literal illustrative value; retain the unaltered source-data definition only'
 if(c[["moderator", exact=TRUE]]%in%c('studlab','slab','label'))reason<-'generated study identifier, not a moderator'
 d<-c[["rows", exact=TRUE]];dd<-d[order(d[["yi", exact=TRUE]],d[["vi", exact=TRUE]],d[["x", exact=TRUE]]),c('yi','vi','x')]
 signature<-paste(c[["dataset", exact=TRUE]],c[["moderator", exact=TRUE]],paste(sprintf('%.17g',as.matrix(dd)),collapse=','),sep='|')
 if(is.null(reason)&&!is.null(seen[[signature]]))reason<-paste('duplicate complete-case numeric configuration of',seen[[signature]])
 if(is.null(reason)){kept[[length(kept)+1]]<-c;seen[[signature]]<-c[["id", exact=TRUE]]}else excluded[[length(excluded)+1]]<-list(id=c[["id", exact=TRUE]],reason=reason)
}
saveRDS(kept,'corpus.rds');writej(kept,'corpus.json');writej(excluded,'configuration-exclusions.json')
cat(length(kept),'final configurations;',length(excluded),'source-audit exclusions\n')
