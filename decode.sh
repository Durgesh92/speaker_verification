. ./cmd.sh
. ./path.sh

set -e
nj=1
nnet_dir=exp/xvector_nnet_1a
trials=exp/xvector_nnet_1a/trials
audio=$1
input_dir=test
mfccdir=$input_dir/exp/mfcc

mkdir -p $input_dir
rm -rf $input_dir
mkdir $input_dir

echo "995-v995_057 $audio" > $input_dir/wav.scp
echo "995-v995_057 spk" > $input_dir/utt2spk
echo "spk 995-v995_057" > $input_dir/spk2utt

if [ -f exp/xvector_nnet_1a/trials ]; then
	ll=0
#	echo "Found trials...."
else
	cd exp/xvector_nnet_1a/
	tar -xvzf trials.tgz
	cd -
fi

steps/make_mfcc.sh --write-utt2num-frames true --mfcc-config conf/mfcc.conf --nj $nj --cmd "$train_cmd" \
	$input_dir $input_dir/exp/make_mfcc $mfccdir || exit 0;

utils/fix_data_dir.sh $input_dir || exit 0;

sid/compute_vad_decision.sh --nj $nj --cmd "$train_cmd" \
	$input_dir $input_dir/exp/make_vad $mfccdir || exit 0;

utils/fix_data_dir.sh $input_dir || exit 0;

sid/nnet3/xvector/extract_xvectors.sh --cmd "$train_cmd --mem 4G" --nj $nj \
	$nnet_dir $input_dir \
	$input_dir/exp/xvectors_test || exit 0;

ivector-subtract-global-mean \
	$nnet_dir/xvectors_train/mean.vec \
	scp:$nnet_dir/xvectors_train/spk_xvector.scp \
	ark:- | transform-vec $nnet_dir/xvectors_train/transform.mat ark:- \
	ark: | ivector-normalize-length ark:- ark,t:$nnet_dir/train_global_mean.ark || exit 0;

ivector-subtract-global-mean \
        $nnet_dir/xvectors_train/mean.vec \
        scp:$input_dir/exp/xvectors_test/xvector.scp \
        ark:- | transform-vec $nnet_dir/xvectors_train/transform.mat ark:- \
        ark: | ivector-normalize-length ark:- ark,t:$input_dir/test_global_mean.ark || exit 0;


#$train_cmd $input_dir/exp/test_scoring.log \
#       ivector-plda-scoring --normalize-length=true \
#       "$nnet_dir/xvectors_train/plda" \
#       "ark:$nnet_dir/train_global_mean.ark" \
#       "ark:$input_dir/test_global_mean.ark" \
#       "cat '$trials' | cut -d\  --fields=1,2 |" $input_dir/exp/scores_test || exit 0;

python3 compute_cosin.py test/test_global_mean.ark
#echo "*************************"
#python local/select_speaker.py $input_dir/exp/scores_test
#echo "*************************"
#echo "Done"
