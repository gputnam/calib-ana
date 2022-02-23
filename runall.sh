path=/pnfs/icarus/persistent/calibration/calib_ntuples/data/run
savedir=/icarus/data/users/gputnam/drift-normalization

for dir in $path/*/
do
  dir=${dir%*/}
  dirname="${dir##*/}"
  if test $dirname -lt 60
  then
    continue
  fi

  for subdir in $dir/*/
  do
    subdir=${subdir%*/}
    subdirname="${subdir##*/}"
    nfile=`ls $subdir | grep root | wc -l`
    echo "Starting Run ${dirname}${subdirname} NFile: ${nfile}"

    if test $nfile -eq 0
    then
      echo "Skipping..."
      continue
    fi

    python make_etau_df.py $savedir/drift_${dirname}${subdirname}.df $subdir/*.root
    echo "Finished Run ${dirname}${subdirname}"
    echo "Saved file: $savedir/drift_${dirname}${subdirname}.df"
  done
done

  
