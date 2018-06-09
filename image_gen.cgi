#!/usr/bin/perl
#
# 確認lキー用画像表示モジュール

require './keyinit.pl';
use Image::Magick;
#use Crypt::CBC;

# パラメータ受け取り
$val = $ENV{'QUERY_STRING'};
$val =~ s/<//g;
$val =~ s/>//g;
$val =~ s/"//g;
$val =~ s/&//g;
$val =~ s/\s//g;
$val =~ s/\r\n//g;
$val =~ s/\r//g;
$val =~ s/\n//g;

# 確認キーデコード
($text,$old_time) = &de_key($val);
if($space){ $text =~ s/(\w)/$1 /g; chomp($text); }

# 文字画像作成
$image = Image::Magick->new;

# バックグラウンド画像読み込み
$tail = "1";
if ($bgfile =~ /\.gif$/i) { $tail = "0"; }
if ($bgfile =~ /\.jpe?g$/i && $tail) { $tail="0"; }
if(!$tail){
	$status = $image->Read($bgfile);
	warn($status) if($status);}
else{
	# 指定色のキャンバスを作成
	$CH = $H +20;
	$image->Set(size=>"$W x $CH");
	$image->ReadImage("xc:$bgfile");
}

# 文字データ書込み
$image->Annotate(text=>"$text", fill=>"$font_color",
                 font=>"$font", pointsize=>"$font_size",
                 gravity=>"center");

# 画像書き出し
$pr_image = 'char-' . "$imgfile";
$image->Write($pr_image) if ($debug);

# 波状加工
$image->Wave("$amp x $pitch") if ($amp || $pitch); 

# 画像書き出し
$pr_image = 'wave-' . "$imgfile";
$image->Write($pr_image) if ($debug);

# 画像トリミング
$vert = $vert + 12;
$image->Crop(width=>"$W", height=>"$H" ,x=>"0", y=>"$vert");
# 画像サイズ情報修正
$image->Set(page=>"$W x $H + 0 + 0");

# 画像書き出し
$image->Write($imgfile) if ($debug);

# 画像送信
print "Content-type: image/gif\n\n";
binmode(STDOUT);
$image->Write("gif:-");

undef $image;

exit;
