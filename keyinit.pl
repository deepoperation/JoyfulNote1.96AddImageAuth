# �m�F�L�[�摜�����֘A�X�N���v�g

#use Crypt::CBC;

#-----�ݒ�--------------------------------------------------#
# �f�o�b�N���[�h
# �f�o�b�N���ɉ摜�t�@�C���𐶐��B
# ���ׂ��d���Ȃ�̂ŏ�p�s�B
$debug = 0;    # 1:�f�o�b�N���[�h
# �f�o�b�N���ɐ�������m�F�L�[�摜�t�@�C��
$imgfile = 'bbs.gif';

# �m�F�L�[�L������(��)
$ef_time = '30';

# �Í����L�[(4�`8���F�p�召����+����)
$crypt_key = '1234ABcd';

# �m�F�L�[����
$len = '3';
# �m�F�L�[�������
# 0=�p�啶��, 1=�p������, 2=����, 3=�p�召����+����
# ���݂�����ƌ딻�ʂ��₷���Ȃ�̂�3�͋ɗ͎g�p���Ȃ����ƁB
$chr = 0;          
@charset = ('�p�啶��','�p������','����','�p�召����+����');

# �����摜�̕��ƍ���
$W = '60';  # ��
$H = '22';  # ����

# �o�b�N�O���E���h�摜�t�@�C��
# �P��F�̃L�����o�X�������������邩�A�\�ߗp�ӂ��ꂽ�摜���w��
# �摜(gif/jpg�`���̂�)�𗘗p����ꍇ�́A�����摜�̍���+20�s�N�Z�����x
# �̉摜��p�ӂ��邱�ƁB
$bgfile = '#ffffff';   # �L�����o�X�F
#$bgfile = 'bg.gif';   # �摜�t�@�C����

# �摜�����Ɏg�p����t�H���g�̃p�X
# truetype�t�H���g���΃p�X�Ŏw�肷�邱�ƁB
# �g�^���H����ꍇ�́A������I�΂Ȃ��Ɣ��Ǖs�\�ɂȂ�B
# (CentOS��truetype�t�H���g�͂قƂ�Ǔ����Ă��Ȃ��̂ŁA
#  �ʓr�ARHEL��SRPM�����r���h���ăC���X�g�[������Ɨǂ��B)
# SuSE9.3
#$font = '/usr/X11R6/lib/X11/fonts/truetype/luxirb.ttf';
# SuSE10.2
#$font = '/usr/share/fonts/truetype/luxirb.ttf';
# CentOS4.4
#$font = '/usr/X11R6/lib/X11/fonts/TTF/luxirb.ttf';
# WindowsXP
$font = 'C:\WINDOWS\Fonts\TIMESBD.TTF';

# �t�H���g�F
$font_color = '#ee0000';
# �t�H���g�T�C�Y
$font_size = '20';
# �������l�܂��ĕ����摜������ꍇ�̕����Ԓ���
$space = '0';  # 0:�Ȃ� 1:����(�X�y�[�X�}��)
# �����̍��������̔�����(�f�t�H���g:0, ������ ex. '-2')
$vert  = '0';
 
# �����摜�̔g����H�̐U���ƃs�b�`
# �g����H���Ȃ��ꍇ�͗����Ƃ�0�ɂ��邱��
$amp   = '1';    # �U��
$pitch = '10';   # �s�b�`
#$amp    = '0';    # �g����H���Ȃ��ꍇ�͗����Ƃ�0�ɂ��邱��
#$pitch  = '0';

#-----�ݒ�I��----------------------------------------------#

#----------------------#
# �����_���e�L�X�g���� #
#----------------------#
sub random_text {
#(����, �g�p�������)
	my($len, $chr) = @_;
	my(@str, $ciphertext);
	my $text='';
	if(!$chr){ @str=('A'..'Z'); }        # �p�啶��
	elsif($chr == 1){ @str=('a'..'z'); } # �p������
	elsif($chr == 2){ @str=('0'..'9'); } # ����
	else{ @str=('A'..'Z','a'..'z','0'..'9',); } # �p�召����+����

	$len = 8 if (!$len);
	for (1 .. $len) {
		$text .= $str[int rand($#str+1)];
	}
	return $text;
}

#--------------------#
# �m�F�L�[�`�F�b�N   #
#--------------------#
sub key_chk {
#(�m�F�L�[,�Í��L�[)
	my($chk, $key) = @_;
	my($plaintext,$old_time);
	if (!$chk){&error("�L�[���[�h����͂��Ă�������");}
	# �G���R�[�h
	($plaintext,$old_time) = &de_key($key);

	# �L�[��v
	if ($chk eq $plaintext) {
		# �������ԃI�[�o�[
		if(time - $old_time > $ef_time*60){ &error("�������Ԃ��I�[�o���Ă��܂�"); }
		# ��������OK
		else{ return 1; }
	# �L�[�s��v
	}else{ &error("�L�[���[�h������Ă��܂�"); }
}

#--------------------#
# �m�F�L�[�G���R�[�h #
#--------------------#
sub en_key {
	my($text,$cipher,$ciphertext);
	$text = &random_text($len,$chr);
	$text .= time;
	# �G���R�[�h
#	$cipher = Crypt::CBC->new($crypt_key, 'DES');
#	$ciphertext = $cipher->encrypt_hex($text);
	$ciphertext=&pcp_encode($text,$crypt_key);
	return ($ciphertext);
}

#--------------------#
# �m�F�L�[�f�R�[�h�@ #
#--------------------#
sub de_key {
#(�m�F�L�[)
	my($ciphertext,$cipher,$plaintext);
	$ciphertext = $_[0];
	# �f�R�[�h
#	$cipher = Crypt::CBC->new($crypt_key, 'DES');
#	$plaintext = $cipher->decrypt_hex($ciphertext);
	$plaintext=&pcp_decode($ciphertext,$crypt_key);
	# �m�F�L�[�ƕ\���������Ԃ𒊏o
	$plaintext =~ /^(\w{$len})(\d+)/;
	return ($1,$2); # (�m�F�L�[,����)
}

############################################################
# Perl-CGI�p�@�ȈՈÍ��T�u���[�`�� Ver1.1 (2000/11/27�C��)
#
# Copyright (C) 2000 Suzuki Yui
#
# �g����:
#
# �Í����̕��@
# �Í������������b�Z�[�W $message
# �p�X���[�h $password
# �ɑ΂��āA
# $crypt_msg=&pcp_encode($message,$password);
# �Ƃ���΁A�Í������ꂽ���b�Z�[�W$crypt_msg���ł���B

# �������̕��@
# �Í������ꂽ���b�Z�[�W $crypt_msg
# �p�X���[�h $password
# �ɑ΂��āA
# $message=&pcp_decode($crypt_msg,$password);
# �Ƃ���΁A���̃��b�Z�[�W$message���ł���B
#
#

sub pcp_decode {
  my($comment,$key,$i,$j,@key);
  $comment = $_[0];
  $key = $_[1];
  @key = split(//,$key);
  $i = 0;
  $j =  &pcp_make_Table($key);
  $comment=~ s/./$pcp_table{$&}/g;
  $comment =~ s/.../sprintf("%c",oct($&)^(ord($key[$i++ % @key]) +($j++ % 383)))/ges;
  $comment=~s/\0$//;
  return $comment;
}

sub pcp_encode {
  my($comment,$key,$i,$j,@key);
  $comment = $_[0];
  $key = $_[1];
  $comment .="\0" if(length($comment) % 2);
  @key = split(//,$key);
  $i = 0;
  $j =  &pcp_make_Table($key);
  $comment =~ s/./sprintf("%03o",ord($&)^(ord($key[$i++ % @key])+($j++ % 383)))/ges;
  $comment=~ s/../$pcp_table{$&}/g;
  return $comment;
}

# z - 7a (122/512) 389�ȉ�

sub pcp_make_Table{
  my(@list,$i,$j,$k,$init_j,@key,@seed);

  @seed = split(//,'q1aZ.XzS5xACs27wD6eE4d8c0_WvQfRFr9Gt3TgBVbNMnJhyKIujUmYkHiLlOoPp');
  @key = split(//,$_[0]);
  $k=@key;
  $init_j=0;
  for($i=0;$i<64;$i++){
    $j=ord($key[$i % $k]);
    $init_j +=$j;
    $list[$i]=splice(@seed,(($j+$k) % (64-$i)),1);
  }

  $k=0;
  for($i=0;$i<8;$i++){
    for($j=0;$j<8;$j++,$k++){
      $pcp_table{"$i$j"}=$list[$k];
      $pcp_table{$list[$k]}="$i$j";
    }
  }
  return ($init_j % 383);
}

1;
