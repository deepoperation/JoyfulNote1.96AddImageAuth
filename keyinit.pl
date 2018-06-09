# 確認キー画像生成関連スクリプト

#use Crypt::CBC;

#-----設定--------------------------------------------------#
# デバックモード
# デバック時に画像ファイルを生成。
# 負荷が重くなるので常用不可。
$debug = 0;    # 1:デバックモード
# デバック時に生成する確認キー画像ファイル
$imgfile = 'bbs.gif';

# 確認キー有効時間(分)
$ef_time = '30';

# 暗号化キー(4～8桁：英大小文字+数字)
$crypt_key = '1234ABcd';

# 確認キー桁数
$len = '3';
# 確認キー文字種別
# 0=英大文字, 1=英小文字, 2=数字, 3=英大小文字+数字
# 混在させると誤判別しやすくなるので3は極力使用しないこと。
$chr = 0;          
@charset = ('英大文字','英小文字','数字','英大小文字+数字');

# 文字画像の幅と高さ
$W = '60';  # 幅
$H = '22';  # 高さ

# バックグラウンド画像ファイル
# 単一色のキャンバスを自動生成するか、予め用意された画像を指定
# 画像(gif/jpg形式のみ)を利用する場合は、文字画像の高さ+20ピクセル程度
# の画像を用意すること。
$bgfile = '#ffffff';   # キャンバス色
#$bgfile = 'bg.gif';   # 画像ファイル名

# 画像生成に使用するフォントのパス
# truetypeフォントを絶対パスで指定すること。
# 波型加工する場合は、文字を選ばないと判読不能になる。
# (CentOSはtruetypeフォントはほとんど入っていないので、
#  別途、RHELのSRPMをリビルドしてインストールすると良い。)
# SuSE9.3
#$font = '/usr/X11R6/lib/X11/fonts/truetype/luxirb.ttf';
# SuSE10.2
#$font = '/usr/share/fonts/truetype/luxirb.ttf';
# CentOS4.4
#$font = '/usr/X11R6/lib/X11/fonts/TTF/luxirb.ttf';
# WindowsXP
$font = 'C:\WINDOWS\Fonts\TIMESBD.TTF';

# フォント色
$font_color = '#ee0000';
# フォントサイズ
$font_size = '20';
# 文字が詰まって文字画像が見難い場合の文字間調整
$space = '0';  # 0:なし 1:あり(スペース挿入)
# 文字の高さ方向の微調整(デフォルト:0, 負数可 ex. '-2')
$vert  = '0';
 
# 文字画像の波状加工の振幅とピッチ
# 波状加工しない場合は両方とも0にすること
$amp   = '1';    # 振幅
$pitch = '10';   # ピッチ
#$amp    = '0';    # 波状加工しない場合は両方とも0にすること
#$pitch  = '0';

#-----設定終了----------------------------------------------#

#----------------------#
# ランダムテキスト生成 #
#----------------------#
sub random_text {
#(桁数, 使用文字種別)
	my($len, $chr) = @_;
	my(@str, $ciphertext);
	my $text='';
	if(!$chr){ @str=('A'..'Z'); }        # 英大文字
	elsif($chr == 1){ @str=('a'..'z'); } # 英小文字
	elsif($chr == 2){ @str=('0'..'9'); } # 数字
	else{ @str=('A'..'Z','a'..'z','0'..'9',); } # 英大小文字+数字

	$len = 8 if (!$len);
	for (1 .. $len) {
		$text .= $str[int rand($#str+1)];
	}
	return $text;
}

#--------------------#
# 確認キーチェック   #
#--------------------#
sub key_chk {
#(確認キー,暗号キー)
	my($chk, $key) = @_;
	my($plaintext,$old_time);
	if (!$chk){&error("キーワードを入力してください");}
	# エンコード
	($plaintext,$old_time) = &de_key($key);

	# キー一致
	if ($chk eq $plaintext) {
		# 制限時間オーバー
		if(time - $old_time > $ef_time*60){ &error("制限時間をオーバしています"); }
		# 制限時間OK
		else{ return 1; }
	# キー不一致
	}else{ &error("キーワードが誤っています"); }
}

#--------------------#
# 確認キーエンコード #
#--------------------#
sub en_key {
	my($text,$cipher,$ciphertext);
	$text = &random_text($len,$chr);
	$text .= time;
	# エンコード
#	$cipher = Crypt::CBC->new($crypt_key, 'DES');
#	$ciphertext = $cipher->encrypt_hex($text);
	$ciphertext=&pcp_encode($text,$crypt_key);
	return ($ciphertext);
}

#--------------------#
# 確認キーデコード　 #
#--------------------#
sub de_key {
#(確認キー)
	my($ciphertext,$cipher,$plaintext);
	$ciphertext = $_[0];
	# デコード
#	$cipher = Crypt::CBC->new($crypt_key, 'DES');
#	$plaintext = $cipher->decrypt_hex($ciphertext);
	$plaintext=&pcp_decode($ciphertext,$crypt_key);
	# 確認キーと表示した時間を抽出
	$plaintext =~ /^(\w{$len})(\d+)/;
	return ($1,$2); # (確認キー,時間)
}

############################################################
# Perl-CGI用　簡易暗号サブルーチン Ver1.1 (2000/11/27修正)
#
# Copyright (C) 2000 Suzuki Yui
#
# 使い方:
#
# 暗号化の方法
# 暗号化したいメッセージ $message
# パスワード $password
# に対して、
# $crypt_msg=&pcp_encode($message,$password);
# とすれば、暗号化されたメッセージ$crypt_msgができる。

# 復号化の方法
# 暗号化されたメッセージ $crypt_msg
# パスワード $password
# に対して、
# $message=&pcp_decode($crypt_msg,$password);
# とすれば、元のメッセージ$messageができる。
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

# z - 7a (122/512) 389以下

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
