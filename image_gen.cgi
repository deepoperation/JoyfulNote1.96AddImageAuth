#!/usr/bin/perl
#
# �m�Fl�L�[�p�摜�\�����W���[��

require './keyinit.pl';
use Image::Magick;
#use Crypt::CBC;

# �p�����[�^�󂯎��
$val = $ENV{'QUERY_STRING'};
$val =~ s/<//g;
$val =~ s/>//g;
$val =~ s/"//g;
$val =~ s/&//g;
$val =~ s/\s//g;
$val =~ s/\r\n//g;
$val =~ s/\r//g;
$val =~ s/\n//g;

# �m�F�L�[�f�R�[�h
($text,$old_time) = &de_key($val);
if($space){ $text =~ s/(\w)/$1 /g; chomp($text); }

# �����摜�쐬
$image = Image::Magick->new;

# �o�b�N�O���E���h�摜�ǂݍ���
$tail = "1";
if ($bgfile =~ /\.gif$/i) { $tail = "0"; }
if ($bgfile =~ /\.jpe?g$/i && $tail) { $tail="0"; }
if(!$tail){
	$status = $image->Read($bgfile);
	warn($status) if($status);}
else{
	# �w��F�̃L�����o�X���쐬
	$CH = $H +20;
	$image->Set(size=>"$W x $CH");
	$image->ReadImage("xc:$bgfile");
}

# �����f�[�^������
$image->Annotate(text=>"$text", fill=>"$font_color",
                 font=>"$font", pointsize=>"$font_size",
                 gravity=>"center");

# �摜�����o��
$pr_image = 'char-' . "$imgfile";
$image->Write($pr_image) if ($debug);

# �g����H
$image->Wave("$amp x $pitch") if ($amp || $pitch); 

# �摜�����o��
$pr_image = 'wave-' . "$imgfile";
$image->Write($pr_image) if ($debug);

# �摜�g���~���O
$vert = $vert + 12;
$image->Crop(width=>"$W", height=>"$H" ,x=>"0", y=>"$vert");
# �摜�T�C�Y���C��
$image->Set(page=>"$W x $H + 0 + 0");

# �摜�����o��
$image->Write($imgfile) if ($debug);

# �摜���M
print "Content-type: image/gif\n\n";
binmode(STDOUT);
$image->Write("gif:-");

undef $image;

exit;
