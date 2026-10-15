# Experimental LS comparisons never determine the primary numerical verdict.
compare_ls <- function(corpus,app,fresh) {
  rows<-list();i<-0L
  add<-function(id,q,a,b,tol=1e-6,nullable=FALSE,boolean=FALSE) {
    if(is.null(a))a<-list(NULL) else if(!is.list(a))a<-as.list(a)
    if(is.null(b))b<-list(NULL) else if(!is.list(b))b<-as.list(b)
    if(length(a)!=length(b)||length(a)<1)stop('LS vector cardinality')
    # Only R's documented NA (undefined inference) becomes explicit null.
    b<-lapply(b,function(v)if(is.numeric(v)&&length(v)==1&&is.na(v)&&!is.nan(v))NULL else v)
    dif<-mapply(function(x,y) {
      if(is.null(x)||is.null(y)) {
        if(!nullable)stop('Unexpected LS null')
        if(!is.null(x)&&!numeric_one(x))stop('Invalid LS value')
        if(!is.null(y)&&!numeric_one(y))stop('Invalid LS value')
        return(if(is.null(x)&&is.null(y))0 else Inf)
      }
      compare_difference(x,y,absolute=endsWith(q,'display'),boolean=boolean)
    },a,b)
    val<-function(v)if(is.null(v))'null' else if(is.logical(v))as.character(as.numeric(v)) else as.character(v)
    i<<-i+1L;rows[[i]]<<-data.frame(configuration=id,quantity=paste0('LS_',q),index=seq_along(a)-1L,App=vapply(a,val,''),R=vapply(b,val,''),Difference=dif,Tolerance=tol,Result=ifelse(dif<=tol,'PASS','FAIL'),Mode='fresh experimental R LS versus archived browser')
  }
  for(id in names(corpus))if(field(field(corpus,id),'k')>=4) {
    a<-field(app,id);al<-field(a,'ls');rl<-field(field(fresh,id),'ls')
    add(id,'fit_status',length(al)>0&&!('error'%in%names(a)),!('error'%in%names(rl)),0,boolean=TRUE)
    if(length(al)>0&&!('error'%in%names(rl))&&!('error'%in%names(a))) {
      for(q in c('beta','betaSE','alpha','alphaSE','logLik','tau2')) {
        n<-if(q=='tau2')field(field(corpus,id),'k') else if(q=='logLik')1 else 2
        av<-field(al,q);if(!is.list(av))av<-as.list(av)
        vec(av,n,nullable=q%in%c('betaSE','alphaSE'))
        add(id,q,av,field(rl,q),nullable=q%in%c('betaSE','alphaSE'))
      }
      for(q in c('beta_lb','beta_ub')) {
        sgn<-if(q=='beta_lb')-1 else 1
        av<-lapply(1:2,function(j){se<-field(al,'betaSE')[[j]];if(is.null(se))NULL else field(al,'beta')[[j]]+sgn*1.959963984540054*se})
        add(id,q,av,field(rl,q),nullable=TRUE)
      }
      cards<-field(a,'stats');labels<-vapply(cards,function(x)field(x,'label'),'');ix<-which(startsWith(labels,'LS \u03b1')&grepl('slope',labels,fixed=TRUE))
      if(length(ix)!=1)stop('Missing LS p card')
      text<-strsplit(field(cards[[ix]],'value'),'p = ',fixed=TRUE)[[1]];if(length(text)!=2)stop('Malformed LS p card')
      av<-if(text[2]=='--')NULL else as.numeric(text[2]);rv<-field(rl,'alpha_p')[2]
      add(id,'alpha_p_display',av,round(rv,3),0,nullable=TRUE)
      for(q in c('tau2_min','tau2_max')) {
        fn<-if(q=='tau2_min')min else max
        add(id,q,fn(unlist(field(al,'tau2'))),fn(field(rl,'tau2')))
      }
    }
  }
  tab<-do.call(rbind,rows)
  write.csv(tab,'outputs/validate_R_LS_table.csv',row.names=FALSE,na='NA')
  for(q in unique(tab[['quantity',exact=TRUE]])) {
    z<-tab[tab[['quantity',exact=TRUE]]==q,,drop=FALSE]
    cat(sprintf('%s experimental: %d/%d pass; max=%.12g\n',q,sum(z[['Result',exact=TRUE]]=='PASS'),nrow(z),max(z[['Difference',exact=TRUE]])))
  }
  cat('LS experimental (fresh fits): ',sum(tab[['Result',exact=TRUE]]=='PASS'),'/',nrow(tab),' checks pass; excluded from primary exit code\n',sep='')
  invisible(tab)
}
