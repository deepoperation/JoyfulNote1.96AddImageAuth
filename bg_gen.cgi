#!/usr/bin/perl

# �m�F�L�[�摜�̃o�b�N�O���E���h�摜�p�̃����_���L�����o�X�������W���[��

require './keyinit.pl';
use Image::Magick;

# �p�X���[�h
$pass = '12345678';  # �s���N���h�~

# �X�N���v�g
$script		= "./bg_gen.cgi";


# �o�b�N�O���E���h
$title		= '�m�F�L�[�摜�p�̃����_���L�����o�X����';

&form_decode;
if ($FORM{'pass'} ne "" && $pass ne "$FORM{'pass'}") {
	&error("�p�X���[�h���Ⴂ�܂�");
}
elsif ($FORM{'pass'} eq "") {

	&header;
	print "<center>�p�X���[�h����͂��ĉ�����\n";
	print "<form action=\"$script\" method=\"POST\">\n";
	print "<input type=password name=pass size=6>";
	print "<input type=submit value=' �F�� '></form>\n";
	print "</center>\n</body></html>\n";
	&footer;
	exit;
}

# �F�؂n�j
if($FORM{'cmd'} eq "�쐬"){
	&bgimg_gen;
	exit;
}
&bgimg_dsp;
exit;

#--------------#
# �t�H�[������ #
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
#  HTML�w�b�_  #
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
#  HTML�t�b�^  #
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
#  �G���[����  #
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
	print "<TD width=\"70\" align=\"center\">���@��</TD>\n";
	print "<TD width=\"150\" align=\"center\">���@�e</TD>\n";
	print "<TD width=\"350\" align=\"center\">���@�l</TD>\n";
	print "</TR>\n";
	print "<TR>\n";
	print "<TD width=\"20\" align=\"center\">1.</TD>\n";
	print "<TD width=\"70\" align=\"left\">�쐬�摜</TD>\n";
	print "<TD width=\"150\" align=\"center\"><img src=\"$fname\"></TD>\n";
	print "<TD width=\"430\" align=\"left\">�쐬���ꂽ�摜</TD>\n";
	print "</TR>\n";
	print "<TR>\n";
	print "<TD width=\"20\" align=\"center\">2.</TD>\n";
	print "<TD width=\"70\" align=\"left\">�t�@�C����</TD>\n";
	print "<TD width=\"150\" align=\"center\"><input type=text size=\"25\" name=\"fname\" value=\"$fname\"></TD>\n";
	print "<TD width=\"430\" align=\"left\">��������L�����o�X�̃t�@�C����(xxx.gif/xxx.jpg)</TD>\n";
	print "</TR>\n";
	print "<TR>\n";
	print "<TD width=\"20\" align=\"center\">3.</TD>\n";
	print "<TD width=\"70\" align=\"left\">�摜�̕�</TD>\n";
	print "<TD width=\"150\" align=\"center\"><input type=text size=\"25\" name=\"w\" value=\"$w\"></TD>\n";
	print "<TD width=\"430\" align=\"left\">��������L�����o�X�̕�(�s�N�Z��)</TD>\n";
	print "</TR>\n";
	print "<TR>\n";
	print "<TD width=\"20\" align=\"center\">4.</TD>\n";
	print "<TD width=\"70\" align=\"left\">�摜�̍���</FONT></TD>\n";
	print "<TD width=\"150\" align=\"center\"><input type=text size=\"25\" name=\"h\" value=\"$h\"></TD>\n";
	print "<TD width=\"430\" align=\"left\">�ŏI�I�ȕ����摜�t�@�C���̍������w�肷��B<br>\n";
	print "���ۂɍ쐬�����摜�t�@�C���̍����́A�g�^���H���l�����A�w�肵������+20�s�N�Z���ō쐬�����B</TD>\n";
	print "</TR>\n";
	print "<TR>\n";
	print "<TD width=\"20\" align=\"center\">5.</TD>\n";
	print "<TD width=\"70\" align=\"left\">���邳</TD>\n";
	print "<TD width=\"150\" align=\"center\"><input type=text size=\"25\" name=\"bright\" value=\"$bright\"></TD>\n";
	print "<TD width=\"430\" align=\"left\">�L�����o�X�̖��邳(�W����100)���w��B���邢�����g�p����ꍇ�͏����Â�(50�`70)���Ȃ��Ƃ͌������B</TD>\n";
	print "</TR>\n";
	print "<TR>\n";
	print "<TD width=\"20\" align=\"center\">6.</TD>\n";
	print "<TD width=\"70\" align=\"left\">�m�C�Y�̍r��</TD>\n";
	print "<TD width=\"150\" align=\"center\"><input type=text size=\"25\" name=\"newsize\" value=\"$newsize\"></TD>\n";
	print "<TD width=\"430\" align=\"left\">�m�C�Y�̍r��(50�`200�B�W����100)���w��B�m�C�Y�͍r��(150�`200)���Ȃ��Ǝ�������B</TD>\n";
	print "</TR>\n";
	print "</TBODY>\n";
	print "</TABLE>\n";
	print "<TABLE border=\"0\" width=\"500\">\n";
	print "<TBODY>\n";
	print "<TR>\n";
	print "<TD>\n";
	print "<br><input type=submit value=\"�쐬\" name=cmd>&nbsp;&nbsp; \n";
	print "�p�����[�^��ݒ�E�ύX���u�쐬�v���N���b�N���Ă��������B<br>\n";
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
	# �����L�����o�X���쐬
	$image->Set(size=>"$WW2 x $WH2");
	$image->Read("xc:white");   # �o�b�N��
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
	# �I�u�W�F�N�g�j��
	undef $image;
	&header;
	print "<FONT color=\"#ee0000\">�o�b�N�O���E���h�摜���쐬���܂����B</FONT><BR><BR>\n";
	print "�g�^���H���l�����A�w�肵������+20�s�N�Z���ō쐬���Ă��܂��B<BR><BR>\n";
	print "<img src=\"$fname\"><BR><BR>\n";
	print "<form action=\"$script\" method=\"POST\">\n";
	print "<input type=hidden name=\"pass\" value=\"$pass\">\n";
	print "<input type=hidden name=\"fname\" value=\"$fname\">\n";
	print "<input type=hidden name=\"w\" value=\"$w\">\n";
	print "<input type=hidden name=\"h\" value=\"$h\">\n";
	print "<input type=hidden name=\"bright\" value=\"$bright\">\n";
	print "<input type=hidden name=\"newsize\" value=\"$newsize\">\n";
	print "<br><input type=submit value=\"�߂�\" name=cmd><br>\n";
	print "<br>�쐬���ʂ��m�F����ɂ́u�߂�v���N���b�N���Ă��������B<br>\n";
	print "</form>\n";
	&footer;
	exit;

}

