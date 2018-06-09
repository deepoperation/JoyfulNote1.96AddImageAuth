#!/usr/local/bin/perl

#┌─────────────────────────────────
#│  JOYFUL NOTE v1.96 (2006/01/18)
#│  Copyright (c) KentWeb
#│  webmaster@kent-web.com
#│  http://www.kent-web.com/
#└─────────────────────────────────
$ver = 'JoyfulNote v1.96';
#┌─────────────────────────────────
#│ [注意事項]
#│ 1. このスクリプトはフリーソフトです。このスクリプトを使用した
#│    いかなる損害に対して作者は一切の責任を負いません。
#│ 2. 設置に関する質問はサポート掲示板にお願いいたします。
#│    直接メールによる質問は一切お受けいたしておりません。
#│ 3. このスクリプトは、method=POST 専用です。	
#│ 4. 同梱のアイコンで、以下のファイルの著作権者は以下のとおりです。
#│    home.gif : mayuRinさん
#│    clip.gif : 牛飼いとアイコンの部屋さん
#└─────────────────────────────────
#
# 【ファイル構成例】
#
#  public_html (ホームディレクトリ)
#      |
#      +-- joyful / joyful.cgi [705]
#            |      joyful.log [606]
#            |      count.dat  [606]
#            |      jcode.pl   [604]
#            |      cgi-lib.pl [604]
#            |      pastno.dat [606]
#            |
#            +-- img  [707] / home.gif, bear.gif, ...
#            |
#            +-- lock [707] /
#            |
#            +-- past [707] / 1.dat [606] ...

#-------------------------------------------------
#  設定項目
#-------------------------------------------------

# ライブラリ取込
require './jcode.pl';
require './cgi-lib.pl';
require './keyinit.pl';
$ciphertext = &en_key;

# タイトル名
$title = "";

# タイトルの文字色
$t_color = "#804040";

# タイトルの文字サイズ
$t_size = '26px';

# 本文の文字フォント
$face = '"MS UI Gothic", "ＭＳ Ｐゴシック", Osaka';

# 本文の文字サイズ
$b_size = '15px';

# 壁紙を指定する場合（http://から指定）
$bg = "";

# 背景色を指定
$bc = "#FEF5DA";

# 文字色を指定
$tx = "#000000";

# リンク色を指定
$lk = "#0000FF";	# 未訪問
$vl = "#800080";	# 訪問済
$al = "#FF0000";	# 訪問中

# 戻り先のURL (index.htmlなど)
$homepage = "";

# 最大記事数 (親記事+レス記事も含めた数）
$max = 200;

# 管理者用マスタパスワード (英数字で８文字以内)
$pass = '';

# 返信がつくと親記事をトップへ移動 (0=no 1=yes)
$topsort = 1;

# 返信にも添付機能を許可する (0=no 1=yes)
$res_clip = 0;

# 画像と記事の位置
#  1 : 画像が左。記事は右から回り込む
#  2 : 画像が下。記事は画像の上に表示。
$imgpoint = 1;

# タイトルにGIF画像を使用する時 (http://から記述)
$t_img = "";
$t_w = 180;	# GIF画像の幅 (ピクセル)
$t_h = 40;	#    〃    高さ (ピクセル)

# ファイルロック形式
# → 0=no 1=symlink関数 2=mkdir関数
$lockkey = 0;

# ロックファイル名
$lockfile = './lock/joyful.lock';

# ミニカウンタの設置
# → 0=no 1=テキスト 2=GIF画像
$counter = 1;

# ミニカウンタの桁数
$mini_fig = 7;

# テキストのとき：ミニカウンタの色
$cnt_color = "#BB0000";

# GIFカウンタのとき：画像までのディレクトリ
# → 最後は必ず / で閉じる
$gif_path = "./img/";
$mini_w = 8;		# 画像の横サイズ
$mini_h = 12;		# 画像の縦サイズ

# カウンタファイル
$cntfile = './count.dat';

# スクリプトのURL
$script = './joyful.cgi';

# ログファイルを指定
# → フルパスで指定する場合は / から記述
$logfile = './joyfullog.cgi';

# アップロードディレクトリ
# → パスの最後は / で終わること
# → フルパスだと / から記述する
$imgdir = './img/';

# アップロードディレクトリのＵＲＬパス
# → パスの最後は / で終わること
$imgurl = "http://www.xxx.xxx/~xxx/img/";
$imgurl = "./img/";

# 添付ファイルのアップロードに失敗したとき
#   0 : 添付ファイルは無視し、記事は受理する
#   1 : エラー表示して処理を中断する
$clip_err = 0;

# 記事 [タイトル] 部の長さ (全角文字換算)
$sub_len = 30;

# メールアドレスの入力必須 (0=no 1=yes)
$in_email = 0;

# 記事の [タイトル] 部の色
$sub_color = "#880000";

# 記事表示部の下地の色
$tbl_color = "#FFFFFF";

# 同一IPアドレスからの連続投稿時間（秒数）
# → 連続投稿などの荒らし対策
# → 値を 0 にするとこの機能は無効になります
$wait = 120;

# １ページ当たりの記事表示数 (親記事)
$p_log = 5;

# 投稿があるとメール通知する (sendmail必須)
#  0 : 通知しない
#  1 : 通知するが、自分の投稿記事はメールしない。
#  2 : 通知する。自分の投稿記事も通知する。
$mailing = 0;

# メールアドレス(メール通知する時)
$mailto = 'xxx@xxx.xxx';

# sendmailパス（メール通知する時）
$sendmail = '/usr/lib/sendmail';

# 他サイトから投稿排除時に指定 (http://から書く)
$base_url = "";

# 文字色の設定（半角スペースで区切る）
$colors = '#800000 #DF0000 #008040 #0000FF #C100C1 #FF80C0 #FF8040 #000080';

# URLの自動リンク (0=no 1=yes)
$autolink = 1;

# タグ広告挿入オプション
# → <!-- 上部 --> <!-- 下部 --> の代わりに「広告タグ」を挿入する。
# → 広告タグ以外に、MIDIタグ や LimeCounter等のタグにも使用可能です。
$banner1 = '<!-- 上部 -->';	# 掲示板上部に挿入
$banner2 = '<!-- 下部 -->';	# 掲示板下部に挿入

# ホスト取得方法
# 0 : gethostbyaddr関数を使わない
# 1 : gethostbyaddr関数を使う
$gethostbyaddr = 1;

# アクセス制限（半角スペースで区切る、アスタリスク可）
#  → 拒否ホスト名を記述（後方一致）【例】*.anonymizer.com
$deny_host = 'd213.osa19nn1fm10.vectant.ne.jp';
#  → 拒否IPアドレスを記述（前方一致）【例】210.12.345.*
$deny_addr = '';

# アップロードを許可するファイル形式
#  0:no  1:yes
$gif   = 1;	# GIFファイル
$jpeg  = 1;	# JPEGファイル
$png   = 1;	# PNGファイル
$text  = 1;	# TEXTファイル
$lha   = 0;	# LHAファイル
$zip   = 0;	# ZIPファイル
$pdf   = 1;	# PDFファイル
$midi  = 1;	# MIDIファイル
$word  = 0;	# WORDファイル
$excel = 0;	# EXCELファイル
$ppt   = 0;	# POWERPOINTファイル
$ram   = 0;	# RAMファイル
$rm    = 0;	# RMファイル
$mpeg  = 0;	# MPEGファイル
$mp3   = 0;	# MP3ファイル

# 投稿受理最大サイズ (bytes)
# → 例 : 102400 = 100KB
$cgi_lib'maxdata = 51200;

# 画像ファイルの最大表示の大きさ（単位：ピクセル）
# → これを超える画像は縮小表示します
$MaxW = 300;	# 横幅
$MaxH = 150;	# 縦幅

# 家アイコンの使用 (0=no 1=yes)
$home_icon = 0;

# アイコン画像ファイル名 (ファイル名のみ)
$IconHome = "home.gif";  # ホーム
$IconClip = "clip.gif";  # クリップ
$IconSoon = "soon.gif";  # COMINIG SOON

# 画像管理者チェック機能 (0=no 1=yes)
# → アップロード「画像」は管理者がチェックしないと表示されない機能です
# → チェックされるまで「画像」は「COMMING SOON」のアイコンが表示されます
$ImageCheck = 1;

# 投稿後の処理
#  → 掲示板自身のURLを記述しておくと、投稿後リロードします
#  → ブラウザを再読み込みしても二重投稿されない措置。
#  → Locationヘッダの使用可能なサーバのみ
$location = '';

# 禁止ワード
#  → コンマで区切って複数指定する（例）$deny_word = 'アダルト,出会い,カップル';
$deny_word = 'http';

#---(以下は「過去ログ」機能を使用する場合の設定です)---#
#
# 過去ログ生成 (0=no 1=yes)
$pastkey = 1;

# 過去ログ用NOファイル
$nofile  = './pastno.dat';

# 過去ログのディレクトリ
# → フルパスなら / から記述（http://からではない）
# → 最後は必ず / で閉じる
$pastdir = './past/';

# 過去ログ１ファイルの行数
# → この行数を超えると次ページを自動生成します
$log_line = 500;

#-------------------------------------------------
#  設定完了
#-------------------------------------------------

# メイン処理
&decode;
$user_agent	= $ENV{'HTTP_USER_AGENT'};	# クライアントがリクエストを発行するときに使用するブラウザ名
if ($mode eq "howto") { &howto; }
elsif ($mode eq "find") { &find; }
elsif ($mode eq "usr_del")
{
	&axscheck;
	&usr_del;
}
elsif ($mode eq "usr_edt")
{
	&axscheck;
	&usr_edt;
}
elsif ($mode eq "regist")
{
	&axscheck;
	&regist;
}
elsif ($mode eq "res")
{
	&axscheck;
	&res_form;
}
elsif ($mode eq "admin") { &admin; }
elsif ($mode eq "past") { &past; }
elsif ($mode eq "check") { &check; }
elsif ($mode eq "viewer") { &viewer; }
&html_log;

#-------------------------------------------------
#  アクセス制限
#-------------------------------------------------
sub axscheck {
	# IP&ホスト取得
	$host = $ENV{'REMOTE_HOST'};
	$addr = $ENV{'REMOTE_ADDR'};
	
	if ($gethostbyaddr && ($host eq "" || $host eq $addr)) {
		$host = gethostbyaddr(pack("C4", split(/\./, $addr)), 2);
	}
	
	# IPチェック
	local($flg);
	foreach ( split(/\s+/, $deny_addr) )
	{
		s/\./\\\./g;
		s/\*/\.\*/g;
		if ($addr =~ /^$_/i) { $flg = 1; last; }
	}
	if ($flg)
	{
		&error("アクセスを許可されていません");

		# ホストチェック
	}
	elsif($host)
	{
	
		foreach ( split(/\s+/, $deny_host) )
		{
			s/\./\\\./g;
			s/\*/\.\*/g;
			
			if ($host =~ /$_$/i) { $flg = 1; last; }
		}
		if ($flg) {
			&error("アクセスを許可されていません");
		}
	}
#	if ($ENV{'HTTP_FROM'}||$ENV{'HTTP_VIA'}||$ENV{'HTTP_X_FORWARDED_FOR'})
#	{
#		&error("proxy経由では書き込みできません");
#	}
	if($host eq "") { $host = $addr; }
}

#-------------------------------------------------
#  記事表示部
#-------------------------------------------------
sub html_log {
	local($ipt,$wh,$i,$flag);

	# ヘッダを出力
	&header;

	# カウンタ処理
	if ($counter) { &counter; }

	# タイトル部
	print "<div align='center'>\n";
	if ($banner1 ne "<!-- 上部 -->") { print "$banner1<p>\n"; }
	if ($t_img eq '') {
		print "<b style=\"font-size:$t_size;color:$t_color;\">$title</b>\n";
	} else {
		print "<img src=\"$t_img\" width=\"$t_w\" height=\"$t_h\" alt=\"$title\">\n";
	}

	# メニュー部
	print "<hr width=\"90%\">\n";
	print "[<a href=\"$homepage\" target=\"_top\">トップに戻る</a>]\n";
	print "[<a href=\"$script?mode=howto\">留意事項</a>]\n";
	print "[<a href=\"$script?mode=find\">ワード検索</a>]\n";
	print "[<a href=\"$script?mode=past\">過去ログ</a>]\n" if ($pastkey);
	print "[<a href=\"$script?mode=admin\">管理用</a>]\n";
	print "<hr width=\"90%\"></div>\n";

	# 投稿フォーム
	&form();
	print "<center><br>\n";

	# 記事展開
	$i=0;
	$flag=0;
	open(IN,"$logfile") || &error("Open Error: $logfile");
	$top = <IN>;
	while (<IN>) {
		($no,$reno,$date,$name,$mail,$sub,$comment,$url,$host,$pw,$color,$tail,$w,$h,$chk) = split(/<>/);

		if ($reno eq "") { $i++; }
		if ($i < $page + 1) { next; }
		if ($i > $page + $p_log) { next; }

		# 題名の長さ
		if (length($sub) > $sub_len*2) {
			$sub = substr($sub,0,$sub_len*2);
			$sub .= "...";
		}

		if ($mail) { $name = "<a href=\"mailto:$mail\">$name</a>"; }
		if ($home_icon && $url) { $url = "<a href=\"http://$url\" target='_blank'><img src=\"$imgurl$IconHome\" border=0 align=top alt='HomePage'></a>"; }
		elsif (!$home_icon && $url) { $url = "&lt;<a href=\"http://$url\" target='_blank'>HOME</a>&gt;"; }

		if (!$reno && $flag) {
			print "</TD></TR></TABLE><br><br>\n";
			$flag=1;
		}
		if (!$reno) {
			print "<TABLE BORDER=1 WIDTH='90%' BGCOLOR=\"$tbl_color\" CELLSPACING=0 CELLPADDING=2><TR><TD>\n";
			$flag=1;
		}

		if ($reno) { print "<hr noshade size=1 width='85%'>\n"; }
		print "<table border=0 cellpadding=2><tr>\n";
		if ($reno) { print "<td rowspan=2 width=40><br></td>"; }

		print "<td valign=top nowrap><font color=\"$sub_color\"><b>$sub</b></font>　";

		if (!$reno) { print "投稿者：<b>$name</b> 投稿日：$date "; }
		else { print "<b>$name</b> - $date "; }

		print "<font color=\"$sub_color\">No.$no</font></td>";
		print "<td valign=top nowrap> &nbsp; $url </td><td valign=top>\n";

		if (!$reno) {
			print "<form action=\"$script\">\n";
			print "<input type=hidden name=mode value=res>\n";
			print "<input type=hidden name=no value=\"$no\">\n";
			print "<input type=submit value='返信'></td></form>\n";
		} else {
			print "<br></td>\n";
		}

		print "</tr></table><table border=0 cellpadding=5><tr>\n";
		if ($reno) { print "<td width=32><br></td>\n"; }

		print "<td>";
		if (!$reno) { print "<blockquote>\n"; }

		# 自動リンク
		if ($autolink) { &auto_link($comment); }
		if ($imgpoint == 1) {
			$ipt="align=left hspace=18";
		} else {
			$ipt="";
			print "<font color=\"$color\">$comment</font>";
		}

		# 添付ファイルが存在する場合
		if ($tail eq ".gif" || $tail eq ".jpg" || $tail eq ".png") {
			if ($ImageCheck && $chk != 1) {
				print "<p><img src=\"$imgurl$IconSoon\">\n";
			} else {
				if ($w && $h) { $wh="width=$w height=$h"; }
				else { $wh=""; }
				print "<p><a href=\"$imgurl$no$tail\" target='_blank'><img src=\"$imgurl$no$tail\" border=0 $ipt $wh></a>\n";
			}
		} elsif ($tail) {
			print "<p><a href=\"$imgurl$no$tail\"><img src=\"$imgurl$IconClip\" border=0 alt='Download:$no$tail'></a> <b>$no$tail</b>\n";
		}

		print "<font color=\"$color\">$comment</font><br clear=all>" if ($imgpoint == 1);
		if (!$reno) { print "</blockquote>\n"; }
		print "</td></tr></table>\n";

	}
	close(IN);
	print "</TD></TR></TABLE></center>\n";

	$next = $page + $p_log;
	$back = $page - $p_log;

	$p_flag=0;
	print "<p><blockquote><table cellpadding=0 cellspacing=0><tr>\n";
	if ($back >= 0) {
		$p_flag=1;
		print "<td><form action=\"$script\" method=\"POST\">\n";
		print "<input type=hidden name=page value=\"$back\">\n";
		print "<input type=submit value=\"前の$p_log件\"></td></form>\n";
	}
	if ($next < $i) {
		$p_flag=1;
		print "<td><form action=\"$script\" method=\"POST\">\n";
		print "<input type=hidden name=page value=\"$next\">\n";
		print "<input type=submit value=\"次の$p_log件\"></td></form>\n";
	}
	# ページ移動ボタン表示
	if ($p_flag) {
		print "<td width=10></td><td>\n";
		$x=1;
		$y=0;
		while ($i > 0) {
			if ($page == $y) { print "<b>[$x]</b>\n"; }
			else { print "[<a href=\"$script?page=$y\">$x</a>]\n"; }
			$x++;
			$y = $y + $p_log;
			$i = $i - $p_log;
		}
		print "</td>\n";
	}
	print "</tr></table></blockquote>\n";
	print "<div align=center>\n";
	print "<form action=\"$script\" method=\"POST\">\n";
	print "<font color=\"$t_color\">- 以下のフォームから自分の投稿記事を修正・削除することができます -</font><br>\n";
	print "処理 <select name=mode>\n";
	print "<option value=usr_edt>修正\n";
	print "<option value=usr_del>削除</select>\n";
	print "記事No <input type=text name=no size=3>\n";
	print "暗証キー <input type=password name=pwd size=4 maxlength=8>\n";
	print "<input type=submit value=\"送信\"></form>\n";

	# 著作権表示部（削除改変不可）
	print "$banner2<p><!-- $ver -->\n";
	print "<span style='font-size:10px;font-family:Verdana,Helvetica,Arial'>\n";
	print "- <a href='http://www.kent-web.com/' target='_top'>Joyful Note</a> -\n";
	print "</span></div>\n</body>\n</html>\n";
	exit;
}

#-------------------------------------------------
#  記事表示部2
#-------------------------------------------------
sub viewer {
	# カウンタ処理
	print "Content-type: text/html\n\n";
	if ($counter) { &counter; }
	# 記事展開
	print "<!-- bansoku start -->\n";
	open(IN,"$logfile") || &error("Open Error: $logfile");
	while (<IN>) {
		($no,$reno,$date,$name,$mail,$sub,$comment,$url,$host,$pw,$color,$tail,$w,$h,$chk) = split(/<>/);
		print "$no<>$reno<>$date<>$name<>$mail<>$sub<>$comment<>$url<>$color<>$tail<>$w<>$h<>$chk<>\n";
	}
	close(IN);
	print "<!-- bansoku end -->\n";
	exit;
}

#-------------------------------------------------
#  投稿記事受付
#-------------------------------------------------
sub regist {
	local($top,$ango,$f,$match,$tail,$W,$H,@lines,@new,@tmp);

	# フォーム入力チェック
	&form_check;

	# 禁止ワードチェック
	if ($deny_word) {
		&deny_word($in{'name'});
		&deny_word($in{'comment'});
	}

	# 時間を取得
	&get_time;

	# クッキーを発行
	&set_cookie($in{'name'},$in{'email'},$in{'url'},$in{'pwd'},$in{'icon'},$in{'color'});

	# ファイルロック
	if ($lockkey) { &lock; }

	# ログを開く
	open(IN,"$logfile") || &error("Open Error: $logfile");
	@lines = <IN>;
	close(IN);

	# 記事NO処理
	$top = shift(@lines);
	local($no,$ip,$time2) = split(/<>/, $top);
	$no++;

	# 連続投稿チェック
	if ($addr eq $ip && $wait > $times - $time2)
		{ &error("連続投稿はもうしばらく時間をおいて下さい"); }

	# 削除キーを暗号化
	if ($in{'pwd'} ne "") { $ango = &encrypt($in{'pwd'}); }

	# ファイル添付処理
	if ($in{'upfile'}) { ($tail,$W,$H) = &upload; }

	# 親記事の場合
	if ($in{'reno'} eq "") {
		$i=0;
		$stop=0;
		foreach (@lines) {
			($no2,$reno2,$d,$n,$m,$s,$com,$u,$ho,$p,$c,$tail2,$w,$h,$chk) = split(/<>/);
			$i++;
			if ($i > $max-1 && $reno2 eq "") { $stop=1; }
			if (!$stop) { push(@new,$_); }
			else {
				if ($pastkey) { push(@data,$_); }
				if (-e "$imgdir$no2$tail2") { unlink("$imgdir$no2$tail2"); }
			}
		}
		unshift(@new,"$no<><>$date<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$host<>$ango<>$in{'color'}<>$tail<>$W<>$H<>0<>\n");
		unshift(@new,"$no<>$addr<>$times<>\n");

		# 過去ログ更新
		if ($data[0]) { &pastlog; }

		# 更新
		open(OUT,">$logfile") || &error("Write Error: $logfile");
		print OUT @new;
		close(OUT);

	# レス記事の場合：トップソートあり
	} elsif ($in{'reno'} && $topsort) {

		$f=0;
		$match=0;
		@new=();
		@tmp=();
		foreach (@lines) {
			($no2,$reno2) = split(/<>/);

			if ($in{'reno'} eq $no2) {
				if ($reno2) { $f++; last; }
				$match=1;
				push(@new,$_);

			} elsif ($in{'reno'} eq $reno2) {
				push(@new,$_);

			} elsif ($match == 1 && $in{'reno'} ne $reno2) {
				$match=2;
				push(@new,"$no<>$in{'reno'}<>$date<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$host<>$ango<>$in{'color'}<>$tail<>$W<>$H<>0<>\n");
				push(@tmp,$_);

			} else { push(@tmp,$_); }
		}
		if ($f || !$match) { &error("不正な返信要求です"); }

		if ($match == 1) {
			push(@new,"$no<>$in{'reno'}<>$date<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$host<>$ango<>$in{'color'}<>$tail<>$W<>$H<>0<>\n");
		}
		push(@new,@tmp);

		# 更新
		unshift(@new,"$no<>$addr<>$times<>\n");
		open(OUT,">$logfile") || &error("Write Error: $logfile");
		print OUT @new;
		close(OUT);

	# レス記事の場合：トップソートなし
	} else {
		$f=0;
		$match=0;
		@new=();
		foreach (@lines) {
			($no2,$reno2) = split(/<>/);

			if ($match == 0 && $in{'reno'} eq $no2) {
				if ($reno2) { $f++; last; }
				$match=1;

			} elsif ($match == 1 && $in{'reno'} ne $reno2) {
				$match=2;
				push(@new,"$no<>$in{'reno'}<>$date<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$host<>$ango<>$in{'color'}<>$tail<>$W<>$H<>0<>\n");
			}
			push(@new,$_);
		}
		if ($f || !$match) { &error("不正な返信要求です"); }

		if ($match == 1) {
			push(@new,"$no<>$in{'reno'}<>$date<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$host<>$ango<>$in{'color'}<>$tail<>$W<>$H<>0<>\n");
		}

		# 更新
		unshift(@new,"$no<>$addr<>$times<>\n");
		open(OUT,">$logfile") || &error("Write Error: $logfile");
		print OUT @new;
		close(OUT);
	}

	# ロック解除
	if ($lockkey) { &unlock; }

	# メール処理
	if ($mailing == 1 && $in{'email'} ne $mailto) { &mail_to; }
	elsif ($mailing == 2) { &mail_to; }

	# リロード
	if ($location) {
		if ($ENV{'PERLXS'} eq "PerlIS") {
			print "HTTP/1.0 302 Temporary Redirection\r\n";
			print "Content-type: text/html\n";
		}
		print "Location: $location?\n\n";

	} else {
		&header;
		print "<div align=center><hr width=400>\n";
		print "<h3>投稿は正常に処理されました</h3>\n";
		print "<form action=\"$script\">\n";
		print "<input type=submit value='掲示板へ戻る'></form>\n";
		print "<hr width=400></div>\n</body></html>\n";
	}
	exit;
}

#-------------------------------------------------
#  画像アップロード
#-------------------------------------------------
sub upload {
	local($macbin,$fname,$flag,$upfile,$imgfile,$tail,$W,$W2,$H,$H2);

	# 画像処理
	$macbin=0;
	foreach (@in) {
		if (/(.*)Content-type:(.*)/i) { $tail=$2; }
		if (/(.*)filename=\"(.*)\"/i) { $fname=$2; }
		if (/application\/x-macbinary/i) { $macbin=1; }
	}
	$tail =~ s/\r//g;
	$tail =~ s/\n//g;

	# ファイル形式を認識
	$flag=0;
	if ($tail =~ /image\/gif/i && $gif) { $tail=".gif"; $flag=1; }
	if ($tail =~ /image\/p?jpeg/i && $jpeg) { $tail=".jpg"; $flag=1; }
	if ($tail =~ /image\/x-png/i && $png) { $tail=".png"; $flag=1; }
	if ($tail =~ /text\/plain/i && $text) { $tail=".txt"; $flag=1; }
	if ($tail =~ /lha/i && $lha) { $tail=".lzh"; $flag=1; }
	if ($tail =~ /zip/i && $zip) { $tail=".zip"; $flag=1; }
	if ($tail =~ /pdf/i && $pdf) { $tail=".pdf"; $flag=1; }
	if ($tail =~ /audio\/.*mid/i && $midi) { $tail=".mid"; $flag=1; }
	if ($tail =~ /msword/i && $word) { $tail=".doc"; $flag=1; }
	if ($tail =~ /ms-excel/i && $excel) { $tail=".xls"; $flag=1; }
	if ($tail =~ /ms-powerpoint/i && $ppt) { $tail=".ppt"; $flag=1; }
	if ($tail =~ /audio\/.*realaudio/i && $ram) { $tail=".ram"; $flag=1; }
	if ($tail =~ /application\/.*realmedia/i && $rm) { $tail=".rm"; $flag=1; }
	if ($tail =~ /video\/.*mpeg/i && $mpeg) { $tail=".mpg"; $flag=1; }
	if ($tail =~ /audio\/.*mpeg/i && $mp3) { $tail=".mp3"; $flag=1; }

	if (!$flag) {
		if ($fname =~ /\.gif$/i && $gif) { $tail=".gif"; $flag=1; }
		if ($fname =~ /\.jpe?g$/i && $jpeg) { $tail=".jpg"; $flag=1; }
		if ($fname =~ /\.png$/i && $png) { $tail=".png"; $flag=1; }
		if ($fname =~ /\.lzh$/i && $lha) { $tail=".lzh"; $flag=1; }
		if ($fname =~ /\.txt$/i && $text) { $tail=".txt"; $flag=1; }
		if ($fname =~ /\.zip$/i && $zip) { $tail=".zip"; $flag=1; }
		if ($fname =~ /\.pdf$/i && $pdf) { $tail=".pdf"; $flag=1; }
		if ($fname =~ /\.mid$/i && $midi) { $tail=".mid"; $flag=1; }
		if ($fname =~ /\.doc$/i && $word) { $tail=".doc"; $flag=1; }
		if ($fname =~ /\.xls$/i && $excel) { $tail=".xls"; $flag=1; }
		if ($fname =~ /\.ppt$/i && $ppt) { $tail=".ppt"; $flag=1; }
		if ($fname =~ /\.ram$/i && $ram) { $tail=".ram"; $flag=1; }
		if ($fname =~ /\.rm$/i && $rm) { $tail=".rm"; $flag=1; }
		if ($fname =~ /\.mpe?g$/i && $mpeg) { $tail=".mpg"; $flag=1; }
		if ($fname =~ /\.mp3$/i && $mp3) { $tail=".mp3"; $flag=1; }
	}

	# アップロード失敗処理
	if (!$flag || !$fname) {
		if (!$clip_err) { return; }
		else { &error("アップロードできません"); }
	}

	$upfile = $in{'upfile'};

	# マックバイナリ対策
	if ($macbin) {
		$length = substr($upfile,83,4);
		$length = unpack("%N",$length);
		$upfile = substr($upfile,128,$length);
	}

	# 添付データを書き込み
	$imgfile = "$imgdir$no$tail";
	open(OUT,">$imgfile") || &error("アップロード失敗");
	binmode(OUT);
	binmode(STDOUT);
	print OUT $upfile;
	close(OUT);

	chmod (0666, $imgfile);

	# 画像サイズ取得
	if ($tail eq ".jpg") { ($W, $H) = &JpegSize($imgfile); }
	elsif ($tail eq ".gif") { ($W, $H) = &GifSize($imgfile); }
	elsif ($tail eq ".png") { ($W, $H) = &PngSize($imgfile); }

	# 画像表示縮小
	if ($W > $MaxW || $H > $MaxH) {
		$W2 = $MaxW / $W;
		$H2 = $MaxH / $H;
		if ($W2 < $H2) { $key = $W2; }
		else { $key = $H2; }
		$W = int ($W * $key) || 1;
		$H = int ($H * $key) || 1;
	}

	return ($tail,$W,$H);
}

#-------------------------------------------------
#  返信フォーム
#-------------------------------------------------
sub res_form {
	local($f,$no,$reno,$date,$name,$mail,$sub,$com,$url);

	# ヘッダを出力
	&header;

	# ログを読み込み
	$f=0;
	open(IN,"$logfile") || &error("Open Error: $logfile");
	$top = <IN>;

	# 関連記事出力
	print "[<a href=\"javascript:history.back()\">戻る</a>]<p>\n";
	print "- 以下は、記事NO. <B>$in{'no'}</B> に関する <a href='#RES'>返信フォーム</a> です -<hr>\n";
	$flag=0;
	while (<IN>) {
		($no,$reno,$date,$name,$mail,$sub,$com,$url) = split(/<>/);
		if (!$reno) { $com = "<blockquote>$com</blockquote>"; }

		if ($in{'no'} == $no && $reno) { $f++; }
		if ($in{'no'} == $no || $in{'no'} == $reno) {
			if ($in{'no'} == $no) { $resub = $sub; }
			if ($url) { $url = "&lt;<a href=\"http://$url\">HOME</a>&gt;"; }
			if ($reno && !$flag) { print "<blockquote>\n"; $flag=1; }
			print "<font color=$sub_color><b>$sub</b></font> 投稿者：<b>$name</b> 投稿日：$date $url <font color=$sub_color>No.$no</font><br>$com<p>\n";
		}
	}
	close(IN);
	if ($f) { &error("不正な返信要求です"); }
	if ($flag) { print "</blockquote>\n"; }
	print "<hr>\n";

	# タイトル名
	if ($resub !~ /^Re\:/) { $resub = "Re\: $resub"; }

	print "<a name=\"RES\"></a>\n";
	&form("res","","","","","",$resub,"","","","","");
	print "</body>\n</html>\n";
	exit;
}

#-------------------------------------------------
#  デコード処理
#-------------------------------------------------
sub decode {
	local($key,$val);
	undef(%in);

	&ReadParse;
	while ( ($key,$val) = each(%in) ) {

		next if ($key eq "upfile");

		# シフトJISコード変換
		&jcode'convert(*val, "sjis", "", "z");

		# タグ処理
		$val =~ s/&/&amp;/g;
		$val =~ s/"/&quot;/g;
		$val =~ s/</&lt;/g;
		$val =~ s/>/&gt;/g;

		# 改行処理
		$val =~ s/\r\n/<br>/g;
		$val =~ s/\r/<br>/g;
		$val =~ s/\n/<br>/g;

		$in{$key} = $val;
	}
	$mode = $in{'mode'};
	$page = $in{'page'};
	$in{'url'} =~ s/^http\:\/\///;
	if ($in{'sub'} eq "") { $in{'sub'} = "無題"; }
}

#-------------------------------------------------
#  留意事項
#-------------------------------------------------
sub howto {
	if ($in_email) {
		$eml_msg = "記事を投稿する上での必須入力項目は<b>「おなまえ」「Ｅメール」「メッセージ」</b>です。ＵＲＬ、題名、削除キーは任意です。";
	} else {
		$eml_msg = "記事を投稿する上での必須入力項目は<b>「おなまえ」</b>と<b>「メッセージ」</b>です。Ｅメール、ＵＲＬ、題名、削除キーは任意です。";
	}

	$maxkb = int ($cgi_lib'maxdata / 1024);
	if ($gif) { $FILE .= "GIF, "; }
	if ($jpeg) { $FILE .= "JPEG, "; }
	if ($png) { $FILE .= "PNG, "; }
	if ($text) { $FILE .= "TEXT, "; }
	if ($lha) { $FILE .= "LHA, "; }
	if ($zip) { $FILE .= "ZIP, "; }
	if ($pdf) { $FILE .= "PDF, "; }
	if ($midi) { $FILE .= "MIDI, "; }
	if ($word) { $FILE .= "WORD, "; }
	if ($excel) { $FILE .= "EXCEL, "; }
	if ($ppt) { $FILE .= "POWERPOINT, "; }
	if ($rm) { $FILE .= "RM, "; }
	if ($ram) { $FILE .= "RAM, "; }
	if ($mpeg) { $FILE .= "MPEG, "; }
	if ($mp3) { $FILE .= "MP3, "; }
	if ($kif) { $FILE .= "KIF, "; }
	if ($ki2) { $FILE .= "KI2, "; }
	if ($csa) { $FILE .= "CSA, "; }
	if ($bod) { $FILE .= "BOD, "; }
	if ($gbd) { $FILE .= "GBD, "; }
	if ($gam) { $FILE .= "GAM, "; }
	$FILE =~ s/\, $//;

	&header;
	print <<"HTML";
[<a href="$script?">掲示板にもどる</a>]
<table width="100%">
<tr><th bgcolor="#880000">
  <font color="#FFFFFF">掲示板の利用上の注意</font>
</th></tr></table>
<p><center>
<table width="90%" border=1 cellpadding=10>
<tr><td bgcolor="$tbl_color">
<OL>
<li>この掲示板は<b>クッキー対応</b>です。１度記事を投稿いただくと、おなまえ、Ｅメール、ＵＲＬ、削除キーの情報は２回目以降は自動入力されます。（ただし利用者のブラウザがクッキー対応の場合）<p>
<li>画像などのバイナリーファイルをアップロードすることが可能\です。
<p>
  <ul>
  <li>添付可能\ファイル : $FILE
  <li>最大投稿データ量 : $maxkb KB
  <li>画像は横$MaxWピクセル、縦$MaxHピクセルを超えると縮小表\示されます。
  </ul>
<p>
<li>投稿内容には、<b>タグは一切使用できません。</b><p>
<li>$eml_msg<p>
<li>記事には、<b>半角カナは一切使用しないで下さい。</b>文字化けの原因となります。<p>
<li>記事の投稿時に<b>「削除キー」</b>にパスワード（英数字で8文字以内）を入れておくと、その記事は次回<b>削除キー</b>によって削除することができます。<p>
<li>記事の保持件数は<b>最大 $max件</b>です。それを超えると古い順に自動削除されます。<p>
<li>既存の記事に<b>「返信」</b>をすることができます。各記事の上部にある<b>「返信」</b>ボタンを押すと返信用フォームが現れます。<p>
<li>過去の投稿記事から<b>「キーワード」によって簡易検索ができます。</b>トップメニューの<a href="$script?mode=find">「ワード検索」</a>のリンクをクリックすると検索モードとなります。<p>
<br>
</OL>
</td></tr></table>
<br>
<table width="100%">
<tr><th bgcolor="#880000">
  <font color="#FFFFFF">管理規定</font>
</th></tr></table>
<br>
<table width="90%" border=1 cellpadding=10>
<tr><td bgcolor="$tbl_color">
</td></tr></table>
</center>
</body>
</html>
HTML
	exit;
}

#-------------------------------------------------
#  ワード検索処理
#-------------------------------------------------
sub find {
	&header;
	print <<"EOM";
[<a href="$script?">掲示板に戻る</a>]
<p>
<ul>
  <li>検索したい<b>キーワード</b>を入力し、「条件」「表\示」を選択して検索ボタンを押して下さい。
  <li>キーワードは「半角スペース」で区切って複数指定することができます。
<p><form action="$script" method="POST">
<input type=hidden name=mode value="find">
キーワード：<input type=text name=word size=30 value="$in{'word'}">
条件：<select name=cond>
EOM
	if (!$in{'cond'}) { $in{'cond'} = "AND"; }
	foreach ("AND", "OR") {
		if ($in{'cond'} eq "$_") {
			print "<option value=\"$_\" selected>$_\n";
		} else {
			print "<option value=\"$_\">$_\n";
		}
	}
	print "</select>\n";
	print "表\示：<select name=view>\n";
	if ($in{'view'} eq "") { $in{'view'} = $p_log; }
	foreach (5,10,15,20) {
		if ($in{'view'} == $_) {
			print "<option value=\"$_\" selected>$_件\n";
		} else {
			print "<option value=\"$_\">$_件\n";
		}
	}
	print "</select>\n";
	print "<input type=submit value='検索'></form>\n</ul>\n";

	# ワード検索の実行と結果表示
	if ($in{'word'} ne "") {

		# 入力内容を整理
		$in{'word'} =~ s/　/ /g;
		@pairs = split(/\s+/, $in{'word'});

		# ファイルを読み込み
		@new=();
		open(IN,"$logfile") || &error("Open Error : $logfile");
		$top = <IN>;
		while (<IN>) {
			$flag=0;
			foreach $pair (@pairs) {
;				@indexArray = split/<>/;
				
				#@indexArray = splice(@indexArray, 8, 1);
				$indexArray[8] = "";
				$indexArray[9] = "";
				$indexValue = "";
				foreach $arrayValue(@indexArray)
				{
					$indexValue = $indexValue . $arrayValue . "<>";
				}
				
				
				if (index($indexValue, $pair) >= 0) {
					$flag=1;
					if ($in{'cond'} eq 'OR') { last; }
				} else {
					if ($in{'cond'} eq 'AND') { $flag=0; last; }
				}
			}
			if ($flag) { push(@new,$_); }
		}
		close(IN);

		# 検索終了
		$count = @new;
		print "検索結果：<b>$count</b>件\n";
		if ($page eq '') { $page = 0; }
		$end_data = @new - 1;
		$page_end = $page + $in{'view'} - 1;
		if ($page_end >= $end_data) { $page_end = $end_data; }

		$next_line = $page_end + 1;
		$back_line = $page - $in{'view'};

		$enwd = &url_enc($in{'word'});
		if ($back_line >= 0) {
			print "[<a href=\"$script?mode=find&page=$back_line&word=$enwd&view=$in{'view'}&cond=$in{'cond'}\">前の$in{'view'}件</a>]\n";
		}
		if ($page_end ne "$end_data") {
			print "[<a href=\"$script?mode=find&page=$next_line&word=$enwd&view=$in{'view'}&cond=$in{'cond'}\">次の$in{'view'}件</a>]\n";
		}
		print "[<a href=\"$script?mode=find\">検索やり直し</a>]\n";

		foreach ($page .. $page_end) {
			($no,$reno,$date,$name,$email,$sub,$com,$url)
						= split(/<>/, $new[$_]);
			if ($email) { $name = "<a href=\"mailto:$email\">$name</a>"; }
			if ($url) { $url = "&lt;<a href=\"http://$url\" target='_top'>HOME</a>&gt;"; }

			if ($reno) { $no = "$renoへのレス"; }

			# 結果を表示
			print "<hr>[<b>$no</b>] <font color=\"$sub_color\"><b>$sub</b></font>";
			print " 投稿者：<b>$name</b> 投稿日：$date $url<br>\n";
			print "<blockquote>$com</blockquote>\n";
		}
		print "<hr>\n";
	}
	print "</body></html>\n";
	exit;
}

#-------------------------------------------------
#  クッキー発行
#-------------------------------------------------
sub set_cookie {
	local(@cook) = @_;
	local($gmt, $cook, @t, @m, @w);

	@t = gmtime(time + 60*24*60*60);
	@m = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec');
	@w = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');

	# 国際標準時を定義
	$gmt = sprintf("%s, %02d-%s-%04d %02d:%02d:%02d GMT",
			$w[$t[6]], $t[3], $m[$t[4]], $t[5]+1900, $t[2], $t[1], $t[0]);

	# 保存データをURLエンコード
	foreach (@cook) {
		s/(\W)/sprintf("%%%02X", unpack("C", $1))/eg;
		$cook .= "$_<>";
	}

	# 格納
	print "Set-Cookie: JoyfulNote=$cook; expires=$gmt\n";
}

#-------------------------------------------------
#  クッキー取得
#-------------------------------------------------
sub get_cookie {
	local($key, $val, *cook);

	# クッキーを取得
	$cook = $ENV{'HTTP_COOKIE'};

	# 該当IDを取り出す
	foreach ( split(/;/, $cook) ) {
		($key, $val) = split(/=/);
		$key =~ s/\s//g;
		$cook{$key} = $val;
	}

	# データをURLデコードして復元
	foreach ( split(/<>/, $cook{'JoyfulNote'}) ) {
		s/%([0-9A-Fa-f][0-9A-Fa-f])/pack("C", hex($1))/eg;

		push(@cook,$_);
	}
	return (@cook);
}

#-------------------------------------------------
#  エラー処理
#-------------------------------------------------
sub error {
	&unlock if ($lockflag);
	&header if (!$headflag);

	print "<center><hr width=400><h3>ERROR !</h3>\n";
	print "<font color=red>$_[0]</font>\n";
	print "<p><hr width=400></center>\n";
	print "</body></html>\n";
	exit;
}

#-------------------------------------------------
#  管理モード
#-------------------------------------------------
sub admin {
	if ($in{'pass'} eq "") {
		&header;
		print "<center><h4>パスワードを入力して下さい</h4>\n";
		print "<form action=\"$script\" method=\"POST\">\n";
		print "<input type=hidden name=mode value=\"admin\">\n";
		print "<input type=hidden name=action value=\"del\">\n";
		print "<input type=password name=pass size=8>\n";
		print "<input type=submit value=\" 認証 \"></form>\n";
		print "</center>\n</body></html>\n";
		exit;
	}
	if ($in{'pass'} ne $pass) { &error("パスワードが違います"); }

	&header;
	print "[<a href=\"$script?\">掲示板に戻る</a>]\n";
	print "<table width='100%'><tr><th bgcolor=\"#804040\">\n";
	print "<font color=\"#FFFFFF\">管理モード</font>\n";
	print "</th></tr></table>\n";

	# 画像許可
	if ($in{'chk'}) {
		@CHK = split(/\0/, $in{'chk'});

		# ロック処理
		if ($lockkey) { &lock; }

		# 許可情報をマッチングし更新
		@new=();
		open(IN,"$logfile") || &error("Open Error : $logfile");
		$top = <IN>;
		while (<IN>) {
			($no,$reno,$d,$n,$m,$s,$com,$u,$ho,$p,$c,$t,$w,$h,$chk)
								 = split(/<>/);
			foreach $xx (@CHK) {
				if ($no eq $xx) {
					$_ = "$no<>$reno<>$d<>$n<>$m<>$s<>$com<>$u<>$ho<>$p<>$c<>$t<>$w<>$h<>1<>\n";
					last;
				}
			}
			push(@new,$_);
		}
		close(IN);

		# 更新
		unshift(@new,$top);
		open(OUT,">$logfile") || &error("Write Error : $logfile");
		print OUT @new;
		close(OUT);

		# ロック解除
		if ($lockkey) { &unlock; }
	}
	# 削除処理
	if ($in{'del'}) {
		@DEL = split(/\0/, $in{'del'});

		# ロック処理
		if ($lockkey) { &lock; }

		# 削除情報をマッチングし更新
		@new=();
		open(IN,"$logfile") || &error("Open Error: $logfile");
		$top = <IN>;
		while (<IN>) {
			$flag=0;
			($no,$reno,$d,$n,$m,$s,$com,$u,$ho,$p,$c,$tail,$w,$h,$chk)
								 	= split(/<>/);
			foreach $del (@DEL) {
				if ($no eq $del || $reno eq $del) {
					if (-e "$imgdir$no$tail") {
						unlink("$imgdir$no$tail");
					}
					$flag=1;
					last;
				}
			}
			if ($flag == 0) { push(@new,$_); }
		}
		close(IN);

		# 更新
		unshift(@new,$top);
		open(OUT,">$logfile") || &error("Write Error: $logfile");
		print OUT @new;
		close(OUT);

		# ロック解除
		if ($lockkey) { &unlock; }
	}

	# 管理を表示
	if ($page eq "") { $page = 0; }
	print "<p><center><table><tr><td>\n<ul>\n";
	print "<li>記事を削除する場合は「削除」のチェックボックスにチェックを入れ「送信する」を押して下さい。\n";
	print "<li>画像許可を行なう場合は「画像許可」のチェックボックスにチェックを入れ「送信する」を押して下さい。\n";
	print "</ul>\n</td></tr></table>\n";
	print "<form action=\"$script\" method=\"POST\">\n";
	print "<input type=hidden name=mode value=\"admin\">\n";
	print "<input type=hidden name=page value=\"$page\">\n";
	print "<input type=hidden name=pass value=\"$in{'pass'}\">\n";
	print "<input type=hidden name=action value=\"$in{'action'}\">\n";
	print "<input type=submit value=\"送信する\">";
	print "<input type=reset value=\"リセット\">\n";
	print "<p><table border=0 cellspacing=1><tr>\n";
	print "<th nowrap>削除</th><th nowrap>記事NO</th><th>投稿日</th>";
	print "<th>タイトル</th><th>投稿者</th><th>URL</th><th>コメント</th>";
	print "<th>ホスト名</th><th>画像<br>(bytes)</th>\n";

	$line=9;
	if ($ImageCheck) { print "<th>画像<br>許可</th>"; $line=10; }

	print "</tr>\n";

	open(IN,"$logfile") || &error("Open Error: $logfile");
	$top = <IN>;
	$i=0;
	while (<IN>) {
		$img_flag=0;
		($no,$reno,$date,$name,$mail,$sub,$com,$url,$host,$pw,$color,$tail,$w,$h,$chk) = split(/<>/);

		if ($mail) { $name="<a href=\"mailto:$mail\">$name</a>"; }
		($date) = split(/\(/, $date);

		if ($url) { $url = "&lt;<a href=\"http://$url\" target='_top'>Home</a>&gt;"; }
		else { $url = '-'; }

		$com =~ s/<br>//ig;
		$com =~ s/</&lt;/g;
		$com =~ s/>/&gt;/g;
		if (length($com) > 40) {
			$com = substr($com,0,38);
			$com .= "...";
		}
		if (-e "$imgdir$no$tail") {
			if ($tail eq ".gif" || $tail eq ".jpg" || $tail eq ".png") {
				$img_flag = 1;
				$File = "画像";
			} else { $File = "File"; }
			$clip = "<a href=\"$imgurl$no$tail\" target='_blank'>$File</a>";
			$size = -s "$imgdir$no$tail";
			$all += $size;
		} else {
			$clip = "";
			$size = 0;
		}
		if ($reno eq "") { print "<tr><th colspan=$line><hr></th></tr>\n"; }

		# チェックボックス
		print "<tr><th><input type=checkbox name=del value=\"$no\"></th>";
		print "<td align=center>$no</td>";
		print "<td>$date</td><th>$sub</th><th>$name</th>";
		print "<td align=center>$url</td><td>$com</td>";
		print "<td>$host</td><td align=center>$clip<br>($size)</td>\n";
		# 画像許可
		if ($ImageCheck) {
			if ($img_flag == 1 && $chk == 1) {
				print "<th>OK</th>";
			} elsif ($img_flag == 1 && $chk != 1) {
				print "<th><input type=checkbox name=chk value=$no></th>";
			} else {
				print "<td><br></td>";
			}
		}
		print "</tr>\n";
	}
	close(IN);

	print "<tr><th colspan=$line><hr></th></tr>\n";
	print "</table></form>\n";

	$all = int ($all / 1024);
	print "【添付データ総数 ： <b>$all</b> KB】\n";
	print "</center>\n";
	print "</body></html>\n";
	exit;
}

#-------------------------------------------------
#  ユーザ記事削除
#-------------------------------------------------
sub usr_del {
	if ($in{'no'} eq '' || $in{'pwd'} eq '')
		{ &error("記事Noまたは削除キーが入力モレです"); }

	# ロック処理
	if ($lockkey) { &lock; }

	open(IN,"$logfile") || &error("Open Error : $logfile");
	@lines = <IN>;
	close(IN);
	$top = shift(@lines);

	$flag=0;
	foreach (@lines) {
		($no,$reno,$date,$name,$mail,$sub,$com,$url,$host,$pw,$color,$tail,$w,$h,$chk) = split(/<>/);

		if ($flag == 0 && $in{'no'} eq "$no") {
			if ($pw eq '') {
				&error("該当記事には削除キーが設定されていません");
			}
			# 削除キーを照合
			$match = &decrypt("$in{'pwd'}","$pw");
			if ($match ne 'yes') { &error("削除キーが違います"); }

			# 添付ファイル削除
			if (-e "$imgdir$no$tail") { unlink("$imgdir$no$tail"); }

			if ($reno eq "") { $flag=2; }
			else { $flag=1; }
		}
		elsif ($flag == 2 && $in{'no'} eq $reno) {
			if (-e "$imgdir$no$tail") { unlink("$imgdir$no$tail"); }
			next;
		}
		else { push(@new,$_); }
	}
	if ($flag == 0) { &error("該当記事が見当たりません"); }

	# 更新
	unshift(@new,$top);
	open(OUT,">$logfile") || &error("Write Error : $logfile");
	print OUT @new;
	close(OUT);

	# ロック解除
	if ($lockkey) { &unlock; }
}

#-------------------------------------------------
#  記事修正処理
#-------------------------------------------------
sub usr_edt {
	if ($in{'no'} eq '' || $in{'pwd'} eq '') {
		&error("記事Noまたはパスワードが入力モレです");
	}

	if ($in{'action'} eq "edit") {

		# フォーム入力チェック
		&form_check;

		# 禁止ワードチェック
		if ($deny_word) {
			&deny_word($in{'name'});
			&deny_word($in{'comment'});
		}

		# ロック処理
		&lock if ($lockkey);
	}

	$flag=0;
	open(IN,"$logfile") || &error("Open Error : $logfile");
	$top = <IN>;
	while (<IN>) {
		($no,$reno,$date,$name,$mail,$sub,$com,$url,$host,$pw,$color,$tail,$w,$h,$chk) = split(/<>/);

		if ($in{'no'} == $no) {
			$pw2 = $pw;
			$flag=1;
			if ($in{'action'} ne "edit") { last; }
			else {
				$_ = "$no<>$reno<>$date<>$in{'name'}<>$in{'email'}<>$in{'sub'}<>$in{'comment'}<>$in{'url'}<>$host<>$pw<>$in{'color'}<>$tail<>$w<>$h<>$chk<>\n";
			}
		}
		if ($in{'action'} eq "edit") { push(@new,$_); }
	}
	close(IN);
	if (!$flag) { &error("該当の記事が見当たりません"); }
	if ($pw2 eq "") { &error("パスワードが設定されていません"); }
	$check = &decrypt($in{'pwd'}, $pw2);
	if ($check ne "yes") { &error("パスワードが違います"); }

	if ($in{'action'} eq "edit") {
		unshift(@new,$top);
		open(OUT,">$logfile") || &error("Write Error : $logfile");
		print OUT @new;
		close(OUT);

		&unlock if ($lockkey);

		if ($in{'url'}) { $in{'url'} = "<a href=\"http://$in{'url'}\" target=\"_top\">http://$in{'url'}</a>"; }
		if ($in{'email'}) { $in{'email'} = "<a href=\"mailto:$in{'email'}\">$in{'email'}</a>"; }

		&header;
		print "<h4>- 以下のとおり修正が完了しました -</h4>\n";
		print "<table>\n";
		print "<tr><td>名前</td><td>： <b>$in{'name'}</b></td></tr>\n";
		print "<tr><td>e-mail</td><td>： $in{'email'}</td></tr>\n";
		print "<tr><td>題名</td><td>： <b>$in{'sub'}</b></td></tr>\n";
		print "<tr><td>URL</td><td>： $in{'url'}</td></tr></table>\n";
		print "<blockquote><font color=\"$in{'color'}\">$in{'comment'}</font>\n";
		print "</blockquote>\n";
		print "<form action=\"$script\">\n";
		print "<input type=submit value=' 掲示板に戻る '></form>\n";
		print "</body>\n</html>\n";
		exit;
	}

	$com =~ s/<br>/\r/g;

	&header;
	print "[<a href=\"javascript:history.back()\">戻る</a>]\n";
	print "<p>- 変更する部分のみ修正して送信ボタンを押して下さい -<br>\n";
	&form("edit",$no,$reno,$date,$name,$mail,$sub,$com,$url,$host,$pw,$color);
	print "</body>\n</html>\n";
	exit;
}

#-------------------------------------------------
#  フォーム入力チェック
#-------------------------------------------------
sub form_check {
	# 他サイトからのアクセスを排除
	if ($base_url) {
		$baseUrl =~ s/(\W)/\\$1/g;

		$ref = $ENV{'HTTP_REFERER'};
		$ref =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
		if ($ref && $ref !~ /$base_url/i) { &error("不正なアクセスです"); }
	}
	
	if ($in{'comment'} !~ m/[\x80-\x9f\xe0-\xfc]/) { &error("日本語が含まれていません"); }

	# 確認キーチェック
	if ($mode ne "usr_edt") {
		if(index($user_agent, "komaviewer") < 0) {
			&key_chk($in{'chk'},$in{ciphertext});
		}
	}
	# methodプロパティはPOST限定
	if ($ENV{'REQUEST_METHOD'} ne 'POST') { &error("不正な投稿です"); }

	# 入力項目のチェック
	if ($in{'name'} eq "") { &error("名前が入力されていません"); }
	if ($in{'comment'} eq "") { &error("コメントが入力されていません"); }
	if ($in_email) {
		if ($in{'email'} eq "") { &error("Ｅメールが入力されていません"); }
		elsif ($in{'email'} !~ /^[\w\.\-]+\@[\w\.\-]+\.[a-zA-Z]{2,6}$/) {
			&error("Ｅメールの入力内容が不正です");
		}
	}
}

#-------------------------------------------------
#  時間を取得
#-------------------------------------------------
sub get_time {
	$ENV{'TZ'} = "JST-9";
	$times = time;
	($min,$hour,$mday,$mon,$year,$wday) = (localtime($times))[1..6];
	@week = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');

	# 日時のフォーマット
	$date = sprintf("%04d/%02d/%02d(%s) %02d:%02d",
			$year+1900,$mon+1,$mday,$week[$wday],$hour,$min);
}

#-------------------------------------------------
#  カウンタ処理
#-------------------------------------------------
sub counter {
	local($count, $cntup, @count);

	# 閲覧時のみカウントアップ
	if ($mode eq '') { $cntup = 1; } else { $cntup = 0; }

	# カウントファイルを読みこみ
	open(LOG,"+< $cntfile") || &error("Open Error: $cntfile");
	eval "flock(LOG, 2);";
	$count = <LOG>;

	# IPチェックとログ破損チェック
	local($cnt, $ip) = split(/:/, $count);
#	if ($addr eq $ip || $cnt eq "") { $cntup = 0; }

	# カウントアップ
	if ($cntup) {
		$cnt++;
		truncate(LOG, 0);
		seek(LOG, 0, 0);
		print LOG "$cnt:dummy";
	}
	close(LOG);

	# 桁数調整
	while(length($cnt) < $mini_fig) { $cnt = '0' . $cnt; }
	@cnts = split(//, $cnt);

	# GIFカウンタ表示
	if ($counter == 2) {
		foreach (0 .. $#cnts) {
			print "<img src=\"$gif_path$cnts[$_]\.gif\" alt=\"$cnts[$_]\" width=\"$mini_w\" height=\"$mini_h\">";
		}
	}
	# テキストカウンタ表示
	else {
		print "<font color=\"$cnt_color\" face=\"verdana,Times New Roman,Arial\">$cnt</font><br>\n";
	}
}

#-------------------------------------------------
#  ロック処理
#-------------------------------------------------
sub lock {
	# 古いロックは削除する
	if (-e $lockfile) {
		local($mtime) = (stat($lockfile))[9];
		if ($mtime < time - 30) { &unlock; }
	}

	local($retry) = 5;

	# symlink関数式ロック
	if ($lockkey == 1) {
		while (!symlink(".", $lockfile)) {
			if (--$retry <= 0) { &error('LOCK is BUSY'); }
			sleep(1);
		}

	# mkdir関数式ロック
	} elsif ($lockkey == 2) {
		while (!mkdir($lockfile, 0755)) {
			if (--$retry <= 0) { &error('LOCK is BUSY'); }
			sleep(1);
		}
	}
	$lockflag=1;
}

#-------------------------------------------------
#  ロック解除
#-------------------------------------------------
sub unlock {
	if ($lockkey == 1) { unlink($lockfile); }
	elsif ($lockkey == 2) { rmdir($lockfile); }
	$lockflag=0;
}

#-------------------------------------------------
#  メール送信
#-------------------------------------------------
sub mail_to {
	local($mcom,$hp,$msub,$mbody);

	# メールタイトルを定義
	$msub = &base64("[$title : $no] $in{'sub'}");

	# 記事を復元
	$mcom  = $in{'comment'};
	$mcom =~ s/<br>/\n/g;
	$mcom =~ s/&lt;/</g;
	$mcom =~ s/&gt;/>/g;
	$mcom =~ s/&quot;/"/g;
	$mcom =~ s/&amp;/&/g;

	# URL情報
	if ($in{'url'}) { $hp = "http://$in{'url'}"; }
	else { $hp = ""; }

	# メール本文を定義
	$mbody = <<EOM;
投稿日時：$date
ホスト名：$host
ブラウザ：$ENV{'HTTP_USER_AGENT'}

投稿者名：$in{'name'}
Ｅメール：$in{'email'}
ＵＲＬ  ：$hp
タイトル：$in{'sub'}

$mcom
EOM

	# メールアドレスがない場合は管理者メールに置き換え
	if ($in{'email'} eq "") { $email = $mailto; }
	else { $email = $in{'email'}; }

	open(MAIL,"| $sendmail -t -i") || &error("送信失敗");
	print MAIL "To: $mailto\n";
	print MAIL "From: $email\n";
	print MAIL "Subject: $msub\n";
	print MAIL "MIME-Version: 1.0\n";
	print MAIL "Content-type: text/plain; charset=ISO-2022-JP\n";
	print MAIL "Content-Transfer-Encoding: 7bit\n";
	print MAIL "X-Mailer: $ver\n\n";
	foreach ( split(/\n/, $mbody) ) {
		&jcode'convert(*_, 'jis', 'sjis');
		print MAIL $_, "\n";
	}
	close(MAIL);
}

#-------------------------------------------------
#  BASE64変換
#-------------------------------------------------
#	とほほのWWW入門で公開されているルーチンを
#	参考にしました。( http://www.tohoho-web.com/ )
sub base64 {
	local($sub) = @_;
	&jcode'convert(*sub, 'jis', 'sjis');

	$sub =~ s/\x1b\x28\x42/\x1b\x28\x4a/g;
	$sub = "=?iso-2022-jp?B?" . &b64enc($sub) . "?=";
	$sub;
}
sub b64enc {
	local($ch)="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
	local($x, $y, $z, $i);
	$x = unpack("B*", $_[0]);
	for ($i=0; $y=substr($x,$i,6); $i+=6) {
		$z .= substr($ch, ord(pack("B*", "00" . $y)), 1);
		if (length($y) == 2) {
			$z .= "==";
		} elsif (length($y) == 4) {
			$z .= "=";
		}
	}
	$z;
}

#-------------------------------------------------
#  パスワード暗号処理
#-------------------------------------------------
sub encrypt {
	local($inpw) = $_[0];
	local(@SALT, $salt, $encrypt);

	@SALT = ('a'..'z', 'A'..'Z', '0'..'9', '.', '/');
	srand;
	$salt = $SALT[int(rand(@SALT))] . $SALT[int(rand(@SALT))];
	$encrypt = crypt($inpw, $salt) || crypt ($inpw, '$1$' . $salt);
	return $encrypt;
}

#-------------------------------------------------
#  パスワード照合処理
#-------------------------------------------------
sub decrypt {
	local($inpw, $logpw) = @_;
	local($salt, $check);

	$salt = $logpw =~ /^\$1\$(.*)\$/ && $1 || substr($logpw, 0, 2);
	$check = "no";
	if (crypt($inpw, $salt) eq $logpw || crypt($inpw, '$1$' . $salt) eq $logpw)
		{ $check = "yes"; }
	return $check;
}

#-------------------------------------------------
#  HTMLヘッダー
#-------------------------------------------------
sub header {
	$headflag=1;
	print "Content-type: text/html\n\n";
	print <<"EOM";
<html>
<head>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
<STYLE type="text/css">
<!--
body,td,th { font-size:$b_size; font-family:$face }
a:hover { color: $al }
-->
</STYLE>
<title>$title</title></head>
EOM

	if ($bg) {
		print "<body background=\"$bg\" bgcolor=\"$bc\" text=\"$tx\" link=\"$lk\" vlink=\"$vl\" alink=\"$al\">\n";
	} else {
		print "<body bgcolor=\"$bc\" text=\"$tx\" link=\"$lk\" vlink=\"$vl\" alink=\"$al\">\n";
	}
}

#-------------------------------------------------
#  自動URLリンク
#-------------------------------------------------
sub auto_link {
	$_[0] =~ s/([^=^\"]|^)(http\:[\w\.\~\-\/\?\&\+\=\:\@\%\;\#\%]+)/$1<a href=\"$2\" target='_top'>$2<\/a>/g;
}

#-------------------------------------------------
#  過去ログ生成
#-------------------------------------------------
sub pastlog {
	local($past_flag)=0;

	# 過去NOを開く
	open(NO,"$nofile") || &error("Open Error : $nofile");
	$count = <NO>;
	close(NO);

	# 過去ログのファイル名を定義
	$pastfile  = "$pastdir$count\.dat";

	# 過去ログを開く
	open(IN,"$pastfile") || open(IN,"+>$pastfile")  || &error("Open Error : $pastfile");
	@past = <IN>;
	close(IN);

	# 規定の行数をオーバーすると次ファイルを自動生成
	if ($#past > $log_line) {
		$past_flag=1;

		# カウントファイル更新
		$count++;
		open(NO,">$nofile") || &error("Write Error : $nofile");
		print NO $count;
		close(NO);

		$pastfile = "$pastdir$count\.dat";
		@past=();
	}

	@temp=();
	foreach (@data) {
		($pno,$preno,$pdate,$pname,$pmail,$psub,$pcom,$purl,$pho)
								 = split(/<>/);
		if ($pmail) { $pname = "<a href=\"mailto:$pmail\">$pname</a>"; }
		if ($purl) { $purl = "&lt;<a href=\"http://$purl\" target='_top'>HOME</a>&gt;"; }
		if ($preno) { $pno = "Res: $preno"; }

		# 保存記事をフォーマット
		push(@temp,"<hr>[<b>$pno</b>] <font color=\"$sub_color\"><b>$psub</b></font> 投稿者：<b>$pname</b> 投稿日：$pdate $purl<br><blockquote>$pcom</blockquote>\n");
	}

	# 過去ログを更新
	unshift(@past,@temp);
	open(OUT,">$pastfile") || &error("Write Error : $pastfile");
	print OUT @past;
	close(OUT);

	if ($past_flag) { chmod(0666,$pastfile); }
}

#-------------------------------------------------
#  過去ログ
#-------------------------------------------------
sub past {
	open(IN,"$nofile") || &error("Open Error : $nofile");
	$pastno = <IN>;
	close(IN);

	if (!$in{'pastlog'}) { $in{'pastlog'} = $pastno; }

	&header;
	print <<"EOM";
[<a href="$script?">掲示板に戻る</a>]
<table width="100%"><tr><th bgcolor="#880000">
  <font color="#FFFFFF">過去ログ[$in{'pastlog'}]</font>
</th></tr></table>
<p><table border=0><tr><td>
<form action="$script" method="POST">
<input type=hidden name=mode value=past>
過去ログ：<select name=pastlog>
EOM

	$pastkey = $pastno;
	while ($pastkey > 0) {
		if ($in{'pastlog'} == $pastkey) {
			print "<option value=\"$pastkey\" selected>$pastkey Page\n";
		} else {
			print "<option value=\"$pastkey\">$pastkey Page\n";
		}
		$pastkey--;
	}
	print "</select>\n<input type=submit value='移動'></td></form>\n";
	print "<td width=30></td><td>\n";
	print "<form action=\"$script\" method=\"POST\">\n";
	print "<input type=hidden name=mode value=past>\n";
	print "<input type=hidden name=pastlog value=\"$in{'pastlog'}\">\n";
	print "ワード検索：<input type=text name=word size=30 value=\"$in{'word'}\">\n";
	print "条件：<select name=cond>\n";

	foreach ('AND', 'OR') {
		if ($in{'cond'} eq "$_") {
			print "<option value=\"$_\" selected>$_\n";
		} else {
			print "<option value=\"$_\">$_\n";
		}
	}
	print "</select>\n";
	print "表\示：<select name=view>\n";
	if ($in{'view'} eq "") { $in{'view'} = $p_log; }
	foreach (5,10,15,20,25,30) {
		if ($in{'view'} eq "$_") {
			print "<option value=\"$_\" selected>$_件\n";
		} else {
			print "<option value=\"$_\">$_件\n";
		}
	}
	print "</select>\n<input type=submit value='検索'></td></form>\n";
	print "</tr></table>\n";

	# 表示ログを定義
	$in{'pastlog'} =~ s/\D//g;
	$file = "$pastdir$in{'pastlog'}\.dat";

	# ワード検索処理
	if ($in{'word'} ne "") {
		$in{'word'} =~ s/　/ /g;
		@pairs = split(/\s+/, $in{'word'});

		@new=();
		open(IN,"$file") || &error("Open Error : $file");
		while (<IN>) {
			$flag=0;
			foreach $pair (@pairs) {
				if (index($_,$pair) >= 0) {
					$flag=1;
					if ($in{'cond'} eq 'OR') { last; }
				} else {
					if ($in{'cond'} eq 'AND') { $flag=0; last; }
				}
			}
			if ($flag) { push(@new,$_); }
		}
		close(IN);

		$count = @new;
		print "検索結果：<b>$count</b>件\n";
		if ($page eq '') { $page = 0; }
		$end_data = @new - 1;
		$page_end = $page + $in{'view'} - 1;
		if ($page_end >= $end_data) { $page_end = $end_data; }

		$next_line = $page_end + 1;
		$back_line = $page - $in{'view'};

		$enwd = &url_enc($in{'word'});
		if ($back_line >= 0) {
			print "[<a href=\"$script?mode=past&page=$back_line&word=$enwd&view=$in{'view'}&cond=$in{'cond'}&pastlog=$in{'pastlog'}\">前の$in{'view'}件</a>]\n";
		}
		if ($page_end ne "$end_data") {
			print "[<a href=\"$script?mode=past&page=$next_line&word=$enwd&view=$in{'view'}&cond=$in{'cond'}&pastlog=$in{'pastlog'}\">次の$in{'view'}件</a>]\n";
		}
		# 表示開始
		foreach ($page .. $page_end) { print $new[$_]; }
		print "<hr>\n</body></html>\n";
		exit;
	}

	# ページ区切り処理
	$start = $page + 1;
	$end   = $page + $p_log;

	$i=0;
	open(IN,"$file") || &error("Open Error : $file");
	while (<IN>) {
		$flag=0;
		if ($_ =~ /^\<hr\>\[\<b\>\d+\<\/b\>\]/) { $flag=1; $i++; }
		if ($i < $start) { next; }
		if ($i > $end) { last; }

		if ($flag) { print $_; }
		else {
			$_ =~ s/<hr>//ig;
			print "<blockquote>$_</blockquote>\n";
		}
	}
	close(IN);
	print "<hr>\n";

	$next = $page + $p_log;
	$back = $page - $p_log;
	print "<table>\n";
	if ($back >= 0) {
		print "<td><form action=\"$script\" method=\"POST\">\n";
		print "<input type=hidden name=mode value=past>\n";
		print "<input type=hidden name=pastlog value=\"$in{'pastlog'}\">\n";
		print "<input type=hidden name=page value=\"$back\">\n";
		print "<input type=submit value=\"前の$p_log件\"></td></form>\n";
	}
	if ($next < $i) {
		print "<td><form action=\"$script\" method=\"POST\">\n";
		print "<input type=hidden name=mode value=past>\n";
		print "<input type=hidden name=pastlog value=\"$in{'pastlog'}\">\n";
		print "<input type=hidden name=page value=\"$next\">\n";
		print "<input type=submit value=\"次の$p_log件\"></td></form>\n";
	}
	print "</table>\n</body>\n</html>\n";
	exit;
}

#-------------------------------------------------
#  チェックモード
#-------------------------------------------------
sub check {
	&header;
	print "<h2>Check Mode</h2>\n";
	print "<ul>\n";

	# ログパス
	if (-e $logfile) {
		print "<li>ログファイルのパス：OK\n";
		# パーミッション
		if (-r $logfile && -w $logfile) {
			print "<li>ログファイルのパーミッション：OK\n";
		} else { print "<li>ログファイルのパーミッション：NG\n"; }
	} else { print "<li>ログファイルのパス：NG → $logfile\n"; }

	# カウンタログ
	print "<li>カウンタ：";
	if ($counter) {
		print "設定あり\n";
		if (-e $cntfile) { print "<li>カウンタログファイルのパス：OK\n"; }
		else { print "<li>カウンタログファイルのパス：NG → $cntfile\n"; }
	} else { print "設定なし\n"; }

	# ロックディレクトリ
	print "<li>ロック形式：";
	if ($lockkey == 0) { print "ロック設定なし\n"; }
	else {
		if ($lockkey == 1) { print "symlink\n"; }
		else { print "mkdir\n"; }
		($lockdir) = $lockfile =~ /(.*)[\\\/].*$/;
		print "<li>ロックディレクトリ：$lockdir\n";

		if (-d $lockdir) {
			print "<li>ロックディレクトリのパス：OK\n";
			if (-r $lockdir && -w $lockdir && -x $lockdir) {
				print "<li>ロックディレクトリのパーミッション：OK\n";
			} else {
				print "<li>ロックディレクトリのパーミッション：NG → $lockdir\n";
			}
		} else { print "<li>ロックディレクトリのパス：NG → $lockdir\n"; }
	}

	# 画像ディレクトリ
	print "<li>画像ディレクトリ：$imgdir\n";
	if (-d $imgdir) {
		print "<li>画像ディレクトリのパス：OK\n";
		if (-r $imgdir && -w $imgdir && -x $imgdir) {
			print "<li>画像ディレクトリのパーミッション：OK\n";
		} else {
			print "<li>画像ディレクトリのパーミッション：NG → $imgdir\n";
		}
	} else { print "<li>画像ディレクトリ：NG → $imgdir\n"; }

	# 過去ログ
	print "<li>過去ログ：";
	if ($pastkey == 0) { print "設定なし\n"; }
	else {
		print "設定あり\n";

		# NOファイル
		if (-e $nofile) {
			print "<li>NOファイルパス：OK\n";
			if (-r $nofile && -w $nofile) {
				print "<li>NOファイルパーミッション：OK\n";
			} else { print "<li>NOファイルパーミッション：NG → $nofile\n"; }
		} else { print "<li>NOファイルのパス：NG → $nofile\n"; }

		# ディレクトリ
		if (-d $pastdir) {
			print "<li>過去ログディレクトリパス：OK\n";
			if (-r $pastdir && -w $pastdir && -x $pastdir) {
				print "<li>過去ログディレクトリパーミッション：OK\n";
			} else {
				print "<li>過去ログディレクトリパーミッション：NG → $pastdir\n";
			}
		} else { print "<li>過去ログディレクトリパーミッション：NG → $pastdir\n"; }
	}
	print "</ul>\n</body></html>\n";
	exit;
}

#-------------------------------------------------
#  JPEGサイズ認識
#-------------------------------------------------
sub JpegSize {
	local($jpeg) = @_;
	local($t, $m, $c, $l, $W, $H);

	open(JPEG,"$jpeg") || return (0,0);
	binmode JPEG;
	read(JPEG, $t, 2);
	while (1) {
		read(JPEG, $t, 4);
		($m, $c, $l) = unpack("a a n", $t);

		if ($m ne "\xFF") { $W = $H = 0; last; }
		elsif ((ord($c) >= 0xC0) && (ord($c) <= 0xC3)) {
			read(JPEG, $t, 5);
			($H, $W) = unpack("xnn", $t);
			last;
		}
		else {
			read(JPEG, $t, ($l - 2));
		}
	}
	close(JPEG);
	return ($W, $H);
}

#-------------------------------------------------
#  GIFサイズ認識
#-------------------------------------------------
sub GifSize {
	local($gif) = @_;
	local($data);

	open(GIF,"$gif") || return (0,0);
	binmode(GIF);
	sysread(GIF,$data,10);
	close(GIF);

	if ($data =~ /^GIF/) { $data = substr($data,-4); }

	$W = unpack("v",substr($data,0,2));
	$H = unpack("v",substr($data,2,2));
	return ($W, $H);
}

#-------------------------------------------------
#  PNGサイズ認識
#-------------------------------------------------
sub PngSize {
	local($png) = @_;
	local($data);

	open(PNG, "$png") || return (0,0);
	binmode(PNG);
	read(PNG, $data, 24);
	close(PNG);

	$W = unpack("N", substr($data, 16, 20));
	$H = unpack("N", substr($data, 20, 24));
	return ($W, $H);
}

#-------------------------------------------------
#  URLエンコード
#-------------------------------------------------
sub url_enc {
	local($_) = @_;

	s/(\W)/'%' . unpack('H2', $1)/eg;
	s/\s/+/g;
	$_;
}

#-------------------------------------------------
#  投稿フォーム
#-------------------------------------------------
sub form {
	local($type,$no,$reno,$date,$name,$mail,$sub,$com,$url,$host,$pw,$color) = @_;
	local($cnam,$ceml,$curl,$cpwd,$cico,$ccol);

	print "<blockquote>\n";

	## フォーム種別を判別
	# 修正
	if ($type eq "edit") {
		print "<form action=\"$script\" method=\"POST\">\n";
		print "<input type=hidden name=mode value=\"usr_edt\">\n";
		print "<input type=hidden name=action value=\"edit\">\n";
		print "<input type=hidden name=pwd value=\"$in{'pwd'}\">\n";
		print "<input type=hidden name=no value=\"$in{'no'}\">\n";
		$cnam = $name;
		$ceml = $mail;
		$curl = $url;
		$ccol = $color;
	# 返信
	} elsif ($type eq "res") {
		if ($res_clip) {
			print "<form action=\"$script\" method=\"POST\" enctype=\"multipart/form-data\">\n";
		} else {
			print "<form action=\"$script\" method=\"POST\">\n";
		}
		print "<input type=hidden name=mode value=\"regist\">\n";
		print "<input type=hidden name=reno value=\"$in{'no'}\">\n";
		($cnam,$ceml,$curl,$cpwd,$cico,$ccol) = &get_cookie;
	# 新規
	} else {
		print "<form action=\"$script\" method=\"POST\" enctype=\"multipart/form-data\">\n";
		print "<input type=hidden name=mode value=\"regist\">\n";
		($cnam,$ceml,$curl,$cpwd,$cico,$ccol) = &get_cookie;
	}

	print <<"EOM";
<table border=0 cellspacing=0>
<tr>
  <td nowrap><b>おなまえ</b></td>
  <td ><input type=text name=name size=28 value="$cnam"></td>
</tr>
<tr>
  <td nowrap><b>Ｅメール</b></td>
  <td><input type=text name=email size=28 value="$ceml"></td>
</tr>
<tr>
  <td nowrap><b>タイトル</b></td>
  <td nowrap>
    <input type=text name=sub size=36 value="$sub">
<input type=submit value="投稿する"><input type=reset value="リセット">
  </td>
</tr>
<tr>
  <td colspan=2>
    <b>コメント</b><br>
    <textarea cols=56 rows=7 name=comment wrap="soft">$com</textarea>
  </td>
</tr>
<tr>
  <td nowrap><b>ＵＲＬ</b></td>
  <td><input type=text size=50 name=url value="http://$curl"></td>
</tr>
EOM
	# 添付フォーム
#	if ($type eq "" || ($type eq "res" && $res_clip)) {
#		print "<tr><td><b>添付File</b></td>\n";
#		print "<td><input type=file name=upfile size=40></td></tr>\n";
#	}
	# パスワード欄
	if ($type ne "edit") {
		print "<tr><td nowrap><b>暗証キー</b></td>";
		print "<td><input type=password name=pwd size=8 maxlength=8 value=\"$cpwd\"> ";
		print "(英数字で8文字以内)</td></tr>\n";
	}
	print <<"EOCM";
	<tr>
	<td><b>確認キー</b><br><img src="./image_gen.cgi?$ciphertext" alt="確認キー"></td>
	<td><font color="red">投稿時、左に\表\示されている$len文字($charset[$chr])を入力してください。</font><br>
	<input type=text name=chk size=8 value="" maxlength=8> (確認キーは\表\示後<font color="red">$ef_time分間のみ有効</font>です。)</td>
	<input type=hidden name=ciphertext value="$ciphertext">
	</tr>
EOCM
	# 色指定
	print "<tr><td nowrap><b>文字色</b></td><td>\n";
	@col = split(/\s+/, $colors);
	if ($ccol eq "") { $ccol = $col[0]; }
	foreach (@col) {
		if ($ccol eq $_) {
			print "<input type=radio name=color value=\"$_\" checked><font color=\"$_\">■</font>\n";
		} else {
			print "<input type=radio name=color value=\"$_\"><font color=\"$_\">■</font>\n";
		}
	}
	print "</td></tr></table></form>\n";
#	if ($ImageCheck) {
#		print "・画像は管理者が許可するまで「COMING SOON」のアイコンが表\示されます。<br>\n";
#	}
	
	print "</blockquote>\n";
}

#-------------------------------------------------
#  禁止ワード
#-------------------------------------------------
sub deny_word {
	local($word) = @_;

	local($flg);
	foreach ( split(/,+/, $deny_word) ) {
		if (index($word,$_) >= 0) { $flg=1; last; }
	}
	if ($flg) { &error("不適切な投稿のため受理できません<BR>禁止ワード：$deny_word"); }
}


__END__

