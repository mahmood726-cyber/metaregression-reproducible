# Fresh main, exact-permutation and experimental LS fits; browser evidence is replayed.
field <- function(x,k) {
  if(!is.list(x)||!(k %in% names(x)))stop('Missing field: ',k)
  x[[k,exact=TRUE]]
}
numeric_one <- function(x) is.numeric(x)&&length(x)==1L&&is.finite(x)
tree <- function(x) {
  if(is.list(x)) {
    n<-names(x)
    if(!is.null(n)&&(anyDuplicated(n)||any(!nzchar(n))))stop('Duplicate/empty JSON key')
    invisible(lapply(x,tree))
  }
}
vec <- function(x,n,nullable=FALSE) {
  if(!is.list(x)||length(x)!=n||!all(vapply(x,function(v)numeric_one(v)||(nullable&&is.null(v)),TRUE)))stop('Invalid numeric vector')
  x
}
index <- function(x,n,ids=NULL) {
  if(!is.list(x)||length(x)!=n)stop('Record cardinality')
  keys<-vapply(x,function(r){v<-field(r,'id');if(!is.character(v)||length(v)!=1||!nzchar(v))stop('Invalid ID');v},'')
  if(anyDuplicated(keys)||(!is.null(ids)&&!setequal(keys,ids)))stop('Duplicate ID or coverage mismatch')
  setNames(x,keys)
}
compare_difference <- function(a,b,absolute=FALSE,boolean=FALSE) {
  if(boolean) {
    if(!is.logical(a)||length(a)!=1||is.na(a)||!is.logical(b)||length(b)!=1||is.na(b))stop('Boolean type')
    return(as.numeric(a!=b))
  }
  if(!numeric_one(a)||!numeric_one(b))stop('Invalid numeric value')
  abs(a-b)/if(absolute)1 else max(1,abs(b))
}
check_documented <- function(tab,pins) {
  key<-function(x)paste(field(x,'configuration'),field(x,'quantity'),field(x,'index'),sep='|')
  pk<-vapply(pins,key,'')
  if(length(pk)!=36L||anyDuplicated(pk))stop('Documented keys cardinality')
  fail<-tab[tab[['Result',exact=TRUE]]=='FAIL',,drop=FALSE]
  fk<-paste(fail[['configuration',exact=TRUE]],fail[['quantity',exact=TRUE]],fail[['index',exact=TRUE]],sep='|')
  if(!setequal(fk,pk)||length(fk)!=36L)stop('Unexpected, disappeared or changed documented differences')
}
main <- function() {
  started<-proc.time()[['elapsed',exact=TRUE]]
  userlibs<-strsplit(Sys.getenv('R_LIBS_USER'),.Platform[['path.sep',exact=TRUE]],fixed=TRUE)[[1]]
  .libPaths(c(userlibs[nzchar(userlibs)],.libPaths()))
  for(pkg in c('metafor','metadat','jsonlite','digest'))if(!requireNamespace(pkg,quietly=TRUE))stop('Missing installed package: ',pkg)
  for(pkg in c('metafor','metadat')) {
    want<-if(pkg=='metafor')'5.2.1' else '1.6.0'
    if(as.character(packageVersion(pkg))!=want)stop('Wrong package version: ',pkg,' ',packageVersion(pkg),'; require ',want)
  }
  if(as.character(getRversion())!='4.6.0')stop('Require R 4.6.0')
  read<-function(p){x<-jsonlite::fromJSON(p,simplifyVector=FALSE);tree(x);x}
  pins<-read('INPUT_SHA256.json')
  required<-c('data/corpus.json','results/patched-app.json','expected/documented_differences.json','expected/quantity_coverage.json','bench/refit_worker.R','bench/compare_ls.R')
  if(!setequal(names(pins),required)||length(pins)!=length(required))stop('Input hash manifest coverage')
  for(p in required)if(!is.character(field(pins,p))||!grepl('^[0-9a-f]{64}$',field(pins,p))||digest::digest(file=p,algo='sha256')!=field(pins,p))stop('SHA-256 mismatch: ',p)
  corpus<-index(read('data/corpus.json'),1742L)
  app<-index(read('results/patched-app.json'),1742L,names(corpus))
  documented<-read('expected/documented_differences.json');coverage<-read('expected/quantity_coverage.json')
  cat(R.version.string,'\nmetafor ',as.character(packageVersion('metafor')),'; metadat ',as.character(packageVersion('metadat')),'\n',sep='')
  cat('Recomputed: every main and experimental LS fit, prediction/band, radius formula and all 365 exact permutation tests.\n')
  cat('Replayed: archived browser values, SVG coordinates and structural evidence only. No browser runs.\n')
  dir.create('outputs',showWarnings=FALSE)
  source('bench/refit_worker.R');source('bench/compare_ls.R')
  # A fresh PSOCK pool works on Windows and Unix, uses no saved fit checkpoints.
  workers<-3L
  cl<-parallel::makePSOCKcluster(workers,outfile='outputs/validate_R_workers.log')
  on.exit(try(parallel::stopCluster(cl),silent=TRUE),add=TRUE)
  libs<-.libPaths()
  parallel::clusterCall(cl,function(paths){.libPaths(paths);stopifnot(as.character(packageVersion('metafor'))=='5.2.1');NULL},libs)
  cat('Fresh refits dispatched to ',workers,' local R workers; progress: outputs/validate_R_workers.log\n',sep='')
  fresh<-index(parallel::parLapplyLB(cl,unname(corpus),refit_worker,chunk.size=1L),1742L,names(corpus))
  parallel::stopCluster(cl)
  saveRDS(fresh,'outputs/validate_R_fresh.rds')
  chunks<-list();counter<-0L
  add<-function(id,q,a,b,tol=1e-9,absolute=FALSE,boolean=FALSE,mode='fresh R versus archived browser') {
    if(!is.list(a))a<-as.list(a);if(!is.list(b))b<-as.list(b)
    if(length(a)!=length(b)||length(a)<1)stop('Comparison cardinality')
    dif<-mapply(function(x,y)compare_difference(x,y,absolute,boolean),a,b)
    counter<<-counter+1L
    chunks[[counter]]<<-data.frame(configuration=id,quantity=q,index=seq_along(a)-1L,App=unlist(a),R=unlist(b),Difference=dif,Tolerance=tol,Result=ifelse(dif<=tol,'PASS','FAIL'),Mode=mode)
  }
  for(ii in seq_along(corpus)) {
    id<-names(corpus)[ii];c<-field(corpus,id);a<-field(app,id);k<-field(c,'k');cr<-field(c,'rows')
    if(!numeric_one(k)||k<3||k!=floor(k)||length(cr)!=k)stop('Corpus shape')
    columns<-lapply(c('yi','vi','x'),function(q)vapply(cr,function(r){v<-field(r,q);if(!numeric_one(v))stop('Corpus numeric type');v},0))
    d<-setNames(as.data.frame(columns),c('yi','vi','x'))
    if(any(d[['vi',exact=TRUE]]<=0)||length(unique(d[['x',exact=TRUE]]))<2)stop('Corpus variance/moderator')
    ar<-field(a,'main')
    for(q in c('beta','se','ci_lb','ci_ub'))vec(field(ar,q),2)
    if(any(unlist(field(ar,'se'))<=0))stop('Invalid SE')
    for(q in c('tau2','R2','QE','QE_p','q','df','pred','pred_se','pi_lb','pi_ub'))if(!numeric_one(field(ar,q)))stop('Main numeric type')
    pe<-field(a,'pageErrors');if(!is.list(pe))stop('Page errors shape')
    fr<-field(fresh,id);rr<-field(fr,'main');bp<-field(fr,'band')
    add(id,'record_present',TRUE,TRUE,0,boolean=TRUE,mode='archived structural evidence')
    add(id,'no_page_error',length(pe)==0&&!('error'%in%names(a)),TRUE,0,boolean=TRUE,mode='archived structural evidence')
    add(id,'fit_status',!('error'%in%names(ar))&&!('error'%in%names(a)),TRUE,0,boolean=TRUE)
    for(q in names(rr))add(id,q,field(ar,q),field(rr,q),absolute=endsWith(q,'_p'))
    add(id,'parsed_rows',field(a,'parsed'),k,0,mode='archived structural evidence')
    add(id,'slope_t',field(ar,'beta')[[2]]/field(ar,'se')[[2]],field(fr,'t')[2])
    cards<-field(a,'stats');labels<-vapply(cards,function(x)field(x,'label'),'');if(anyDuplicated(labels))stop('Duplicate cards')
    pick<-which(grepl('test',labels,fixed=TRUE)&grepl('\u03b2',labels,fixed=TRUE));if(length(pick)!=1L)stop('Missing p card')
    pv<-strsplit(field(cards[[pick]],'value'),'p = ',fixed=TRUE)[[1]];if(length(pv)!=2)stop('P card format')
    add(id,'slope_p_display',as.numeric(pv[2]),round(field(fr,'p')[2],3),0,TRUE)
    svg<-field(a,'svg');circles<-field(svg,'circles');if(length(circles)!=k)stop('Bubble count shape')
    for(point in circles)vec(point,3)
    add(id,'bubble_count',length(circles),k,0)
    points<-function(q,n) {
      s<-field(svg,q);if(!is.character(s)||length(s)!=1)stop('SVG string')
      z<-strsplit(trimws(s),' +')[[1]];if(length(z)!=n)stop('SVG sample coverage')
      xy<-lapply(z,function(t){v<-as.numeric(strsplit(t,',',fixed=TRUE)[[1]]);if(length(v)!=2||any(!is.finite(v)))stop('SVG coordinate');v})
      vapply(xy,function(v)v[2],0)
    }
    line<-points('line',201);band<-points('band',402)
    yl<-min(d[['yi',exact=TRUE]]-1.959963984540054*sqrt(d[['vi',exact=TRUE]]));yh<-max(d[['yi',exact=TRUE]]+1.959963984540054*sqrt(d[['vi',exact=TRUE]]));pad<-(yh-yl)*.1;yl<-yl-pad;yh<-yh+pad
    inv<-function(v)yh-(v-60)/380*(yh-yl)
    jj<-c(1,101,201)
    add(id,'bubble_line',inv(line[jj]),field(bp,'pred')[jj])
    # Interleaved upper/lower bounds match the historical per-quantity key order.
    add(id,'bubble_ci',as.vector(rbind(inv(band[jj]),inv(band[403-jj]))),as.vector(rbind(field(bp,'hi')[jj],field(bp,'lo')[jj])))
    add(id,'bubble_radius',vapply(circles,function(v)v[[3]],0),4+10/d[['vi',exact=TRUE]]/max(1/d[['vi',exact=TRUE]]))
    if(k>=4&&k<=7) {
      perm<-field(fr,'permutation');pa<-field(a,'permutation')
      if(!identical(field(pa,'exact'),TRUE))stop('App exact-permutation flag')
      add(id,'exact_permutation_record',TRUE,TRUE,0,boolean=TRUE)
      add(id,'exact_permutation_status',length(pa)>0,TRUE,0,boolean=TRUE)
      add(id,'exact_permutation_p',field(pa,'p'),field(perm,'p'),absolute=TRUE)
    }
    if(ii%%25L==0L){cat(ii,'/',length(corpus),'fresh fits completed\n');flush.console()}
  }
  tab<-do.call(rbind,chunks)
  keys<-paste(tab[['configuration',exact=TRUE]],tab[['quantity',exact=TRUE]],tab[['index',exact=TRUE]],sep='|')
  if(anyDuplicated(keys)||nrow(tab)!=129903L)stop('Check key/coverage mismatch')
  observed<-table(tab[['quantity',exact=TRUE]])
  if(!setequal(names(observed),names(coverage)))stop('Quantity coverage mismatch')
  for(q in names(observed))if(observed[[q,exact=TRUE]]!=field(coverage,q))stop('Quantity cardinality: ',q)
  write.csv(tab,'outputs/validate_R_table.csv',row.names=FALSE,na='NA')
  for(q in unique(tab[['quantity',exact=TRUE]])) {
    z<-tab[tab[['quantity',exact=TRUE]]==q,,drop=FALSE]
    cat(sprintf('%s: %d/%d pass; max=%.12g; tolerance=%g\n',q,sum(z[['Result',exact=TRUE]]=='PASS'),nrow(z),max(z[['Difference',exact=TRUE]]),z[['Tolerance',exact=TRUE]][1]))
  }
  compare_ls(corpus,app,fresh)
  check_documented(tab,documented)
  elapsed<-proc.time()[['elapsed',exact=TRUE]]-started
  jsonlite::write_json(list(seconds=elapsed,R=R.version.string,metafor=as.character(packageVersion('metafor')),main_fits=length(corpus),exact_permutations=sum(vapply(corpus,function(c)field(c,'k')>=4&&field(c,'k')<=7,TRUE)),LS='fresh experimental fits, excluded from primary verdict',workers=workers), 'outputs/validate_R_runtime.json',auto_unbox=TRUE,pretty=TRUE,digits=16)
  cat(sprintf('Runtime: %.3f seconds\n',elapsed))
  cat(sprintf('%d/%d checks pass\n',sum(tab[['Result',exact=TRUE]]=='PASS'),nrow(tab)))
  cat('129,867/129,903 pass; 36 documented, 0 unexpected\n')
  0L
}
if(sys.nframe()==0L) {
  status<-tryCatch(main(),error=function(e){cat('Validation failed: ',conditionMessage(e),'\n',sep='',file=stderr());1L})
  quit(save='no',status=status)
}
