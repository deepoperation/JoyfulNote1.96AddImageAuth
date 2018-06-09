#!/usr/bin/perl

# 確認キー画像のバックグラウンド画像用のランダムキャンバス生成モジュール

require './keyinit.pl';
use Image::Magick;

# パスワード
$pass = '12345678';  # 不正起動防止

# スクリプト
$script		= "./bg_gen.cgi";


# バックグラウンド
$title		= '確認キー画像用のランダムキャンバス生成';

&form_decode;
if ($FORM{'pass'} ne "" && $pass ne "$FORM{'pass'}") {
	&error("パスワードが違います");
}
elsif ($FORM{'pass'} eq "") {

	&header;
	print "<center>パスワードを入力して下さい\n";
	print "<form action=\"$script\" method=\"POST\">\n";
	print "<input type=password name=pass size=6>";
	print "<input type=submit value=' 認証 '></form>\n";
	print "</center>\n</body></html>\n";
	&footer;
	exit;
}

# 認証ＯＫ
if($FORM{'cmd'} eq "作成"){
	&bgimg_gen;
	exit;
}
&bgimg_dsp;
exit;

#--------------#
# フォーム処理 #
#--------------#
sub form_decode {
if ($ENV{'REQUEST_METHOD'} eq "POST") {read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});}
else { $buffer = $ENV{'QUERY_STRING'}; }
	@pairs = split(/&/, $buffer);
	foreach $pair (@pairs) {
		($name,$value) = split(/=/, $pair);
		$value =~ tr/+/ /;
		$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
		$value =~ s/</\&lt\;/g;
		$value =~ s/>/\&gt\;/g;
		$value =~ s/\"/\&quot\;/g;
		$value =~ s/<>/\&lt\;\&gt\;/g;
		$value =~ s/<!--(.|\n)*-->//g;
		$FORM{$name} = $value;
	}
$w      = $FORM{w};
$w = $W if (!(defined($w)));
$h      = $FORM{h};
$h = $H if (!(defined($h)));
$fname = $FORM{fname};
$fname = $bgfile if (!(defined($fname)));
$bright = $FORM{bright};
$bright = 100 if (!(defined($bright)));
$newsize = $FORM{newsize};
$newsize = 100 if (!(defined($newsize)));
}

#--------------#
#  HTMLヘッダ  #
#--------------#
sub header {
	print "Content-type: text/html\n\n";
	print <<"EOM";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<HTML lang="ja">
<HEAD>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
<META HTTP-EQUIV="Content-Style-Type" CONTENT="text/css">
<META HTTP-EQUIV="Pragma" content="no-cache"> 
<META HTTP-EQUIV="Cache-Control" content="no-cache"> 
<META HTTP-EQUIV="expires" content="Sun, 10 Jan 1990 01:01:01 GMT">
<TITLE>$title</TITLE>
</HEAD>
<BODY bgcolor="#f8ffffff">
<DIV align=center>
<H2>$title</H2>
<BR><BR>

EOM
}

#--------------#
#  HTMLフッタ  #
#--------------#
sub footer {
	print <<"EOM";
</DIV>
<BR><HR>
</BODY>
</HTML>
EOM
exit;
}

#--------------#
#  エラー処理  #
#--------------#
sub error {
	&header;
	print "<div align=center>";
	print "<h3>ERROR !</h3>";
	print "<font color=red>$_[0]</font>";
	print "</div>";
	&footer;
}

sub bgimg_dsp {
	&header;
	print "<form action=\"$script\" method=\"POST\">\n";
	print "<input type=hidden value=\"$pass\" name=pass>\n";
	print "<TABLE border=\"1\" width=\"700\">\n";
	print "<TBODY>\n";
	print "<TR>\n";
	print "<TD width=\"20\" align=\"center\">No.</TD>\n";
	print "<TD width=\"70\" align=\"center\">項　目</TD>\n";
	print "<TD width=\"150\" align=\"center\">内　容</TD>\n";
	print "<TD width=\"350\" align=\"center\">備　考</TD>\n";
	print "</TR>\n";
	print "<TR>\n";
	print "<TD width=\"20\" align=\"center\">1.</TD>\n";
	print "<TD width=\"70\" align=\"left\">作成画像</TD>\n";
	print "<TD width=\"150\" align=\"center\"><img src=\"$fname\"></TD>\n";
	print "<TD width=\"430\" align=\"left\">作成された画像</TD>\n";
	print "</TR>\n";
	print "<TR>\n";
	print "<TD width=\"20\" align=\"center\">2.</TD>\n";
	print "<TD width=\"70\" align=\"left\">ファイル名</TD>\n";
	print "<TD width=\"150\" align=\"center\"><input type=text size=\"25\" name=\"fname\" value=\"$fname\"></TD>\n";
	print "<TD width=\"430\" align=\"left\">生成するキャンバスのファイル名(xxx.gif/xxx.jpg)</TD>\n";
	print "</TR>\n";
	print "<TR>\n";
	print "<TD width=\"20\" align=\"center\">3.</TD>\n";
	print "<TD width=\"70\" align=\"left\">画像の幅</TD>\n";
	print "<TD width=\"150\" align=\"center\"><input type=text size=\"25\" name=\"w\" value=\"$w\"></TD>\n";
	print "<TD width=\"430\" align=\"left\">生成するキャンバスの幅(ピクセル)</TD>\n";
	print "</TR>\n";
	print "<TR>\n";
	print "<TD width=\"20\" align=\"center\">4.</TD>\n";
	print "<TD width=\"70\" align=\"left\">画像の高さ</FONT></TD>\n";
	print "<TD width=\"150\" align=\"center\"><input type=text size=\"25\" name=\"h\" value=\"$h\"></TD>\n";
	print "<TD width=\"430\" align=\"left\">最終的な文字画像ファイルの高さを指定する。<br>\n";
	print "実際に作成される画像ファイルの高さは、波型加工を考慮し、指定した高さ+20ピクセルで作成される。</TD>\n";
	print "</TR>\n";
	print "<TR>\n";
	print "<TD width=\"20\" align=\"center\">5.</TD>\n";
	print "<TD width=\"70\" align=\"left\">明るさ</TD>\n";
	print "<TD width=\"150\" align=\"center\"><input type=text size=\"25\" name=\"bright\" value=\"$bright\"></TD>\n";
	print "<TD width=\"430\" align=\"left\">キャンバスの明るさ(標準は100)を指定。明るい字を使用する場合は少し暗く(50～70)しないとは見憎い。</TD>\n";
	print "</TR>\n";
	print "<TR>\n";
	print "<TD width=\"20\" align=\"center\">6.</TD>\n";
	print "<TD width=\"70\" align=\"left\">ノイズの荒さ</TD>\n";
	print "<TD width=\"150\" align=\"center\"><input type=text size=\"25\" name=\"newsize\" value=\"$newsize\"></TD>\n";
	print "<TD width=\"430\" align=\"left\">ノイズの荒さ(50～200。標準は100)を指定。ノイズは荒く(150～200)しないと字が見難い。</TD>\n";
	print "</TR>\n";
	print "</TBODY>\n";
	print "</TABLE>\n";
	print "<TABLE border=\"0\" width=\"500\">\n";
	print "<TBODY>\n";
	print "<TR>\n";
	print "<TD>\n";
	print "<br><input type=submit value=\"作成\" name=cmd>&nbsp;&nbsp; \n";
	print "パラメータを設定・変更し「作成」をクリックしてください。<br>\n";
	print "</TD>\n";
	print "</TR>\n";
	print "</TBODY>\n";
	print "</TABLE>\n";
	print "</form>\n";
	&footer;
	exit;

}

sub bgimg_gen {
	$image = Image::Magick->new;
	$WW = $w;
	$WH = $h + 20;
	$m  = 100 / $newsize;
	$WW2 = $WW * $m;
	$WH2 = $WH * $m;
	# 白いキャンバスを作成
	$image->Set(size=>"$WW2 x $WH2");
	$image->Read("xc:white");   # バック白
	$image->AddNoise( noise=>multiplicative );
	$status = $image->Write("a-$fname");
	$image->Modulate(brightness=>$bright, saturation=>50);
	$status = $image->Write("b-$fname");
	$image = $image->Transform(geometry=>$WW);
	$status = $image->Write("c-$fname");
	$image->Crop(width=>"$WW", height=>"$WH" ,x=>"0", y=>"0");
	$image->Set(page=>"$WW x $WH + 0 + 0");
	$status = $image->Write("d-$fname");
	$status = $image->Write("$fname");
	warn($status) if($status);
	# オブジェクト破棄
	undef $image;
	&header;
	print "<FONT color=\"#ee0000\">バックグラウンド画像を作成しました。</FONT><BR><BR>\n";
	print "波型加工を考慮し、指定した高さ+20ピクセルで作成しています。<BR><BR>\n";
	print "<img src=\"$fname\"><BR><BR>\n";
	print "<form action=\"$script\" method=\"POST\">\n";
	print "<input type=hidden name=\"pass\" value=\"$pass\">\n";
	print "<input type=hidden name=\"fname\" value=\"$fname\">\n";
	print "<input type=hidden name=\"w\" value=\"$w\">\n";
	print "<input type=hidden name=\"h\" value=\"$h\">\n";
	print "<input type=hidden name=\"bright\" value=\"$bright\">\n";
	print "<input type=hidden name=\"newsize\" value=\"$newsize\">\n";
	print "<br><input type=submit value=\"戻る\" name=cmd><br>\n";
	print "<br>作成結果を確認するには「戻る」をクリックしてください。<br>\n";
	print "</form>\n";
	&footer;
	exit;

}

