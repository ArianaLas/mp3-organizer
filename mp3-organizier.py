#!/usr/bin/python
# coding=utf-8

# 
# Copyright by:
# -> Patryk Jaworski <skorpion9312@gmail.com>
# -> Ariana Las <ariana.las@gmail.com>
# License: GNU GPLv3
# 

import sys;
import getopt;
import os;
import shutil;
try:
	import stagger;
except:
	print('[E] Unable to load module stagger, please install it (package: aur/python3-stagger-svn in Arch Linux.');
	sys.exit(1);

class organizer:
	__path = '';
	__target = '';
	__verbose = False;
	__recursive = False;
	__copy = False;
	__delete = False;
	__follow = False;
	__force = False;
	__scheme = '{artist}/{album}/{title}';
	__recognizeCovers = False;
	def __init__(self):
		try:
			options, args = getopt.getopt(sys.argv[1:], 'p:rdft:chvs:', ['path=', 'target-directory=', 'scheme=', 'delete', 'force', 'recursive', 'verbose', 'copy', 'help', 'recognize-covers', 'follow']);
			for option, value in options:
				if option in ('-h', '--help'):
					self.usage();
					sys.exit(0);
				elif option in ('-p', '--path'):
					if value[-1] != '/':
						value += '/';
					self.__v('Setting path as %s...' % value);
					self.__path = value;
				elif option in ('-t', '--target-directory'):
					if value[-1] != '/':
						value += '/';
					self.__v('Setting target as %s...' % value);
					self.__target = value;
				elif option in ('-f', '--force'):
					self.__v('Setting option force...');
					self.__force = True;
				elif option in ('-d', '--delete'):
					self.__v('Setting option delete...');
					self.__delete = True;
				elif option in ('-v', '--verbose'):
					self.__verbose = True;
				elif option in ('-r', '--recursive'):
					self.__v('Setting option recursive...');
					self.__recursive = True;
				elif option in ('-c', '--copy'):
					self.__v('Setting option copy...');
					self.__copy = True;
				elif option in ('-s', '--scheme'):
					self.__v('Setting scheme: %s...' % value);
					self.__scheme = value;
				elif option == '--recognize-covers':
					self.__v('Setting option recognize-covers...');
					self.__recognizeCovers = True;
				elif option == '--follow':
					self.__follow = True;
				else:
					self.__v('Setting default scheme...');


		except getopt.GetoptError as err:
			print('[E] Bad options...');
			self.usage();
			sys.exit(1);
		if not self.__path or not self.__target:
			print('[E] You must specify path and target...');
			self.usage();
			sys.exit(1);
		self.__prepare();
		self.__organize(self.__path);

	def usage(self):
		print('========== MP3-ORGANIZER ==========');
		print('Automatically organize, sort or rename your mp3 music collection\n');
		print('Authors:');
		print('   Patryk Jaworski <skorpion9312@gmail.com>\n   Ariana Las <ariana.las@gmail.com>');
		print('\n[E] <- Error\n[W] <- Warning\n[V] <- Verbose\n[I] <- Information\n');
		print('Usage: \n   -t --target-directory\n      specify target directory (required)');
		print('   -p --path\n      specify search directory (required)');
		print('   -d --delete\n      delete directories after all files are moved');
		print('   -f --force\n      force remove unnecessary directories');
		print('   -r --recursive\n      search in directories recursively');
		print('   -c --copy\n      copy files instead of moving');
		print('   -s --scheme\n      specify output files scheme');
		print('       default: {artist}/{album}/{title}');
		print('       available: {artist} {album} {date} {title}\n                  {old-file-name} {genre} {track}');
		print('   -h --help\n      display help');
		print('   -v --verbose\n      enable verbose messages (should be first option)');
		print('   --recognize-covers\n      move/copy all image files');
		print('   --follow\n      follow symlinks');
		print('\nExamples:\n   $ mp3-organizer -p ~/Music/ -t ~/Music/ -r --recognize-covers');
		print('      Organize ~/Music/ directory (do not remove old directories even empty)');
		print('\n   $ mp3-organizer -p ~/ -t ~/Music/ -r -d');
		print('      Find all music (mp3) files in your home directory and move them to ~/Music/\n      (use default scheme)');

	def __prepare(self):
		self.__v('Preparing directories...');
		try:
			self.__v('Checking path...');
			if not os.path.exists(self.__path):
				raise Exception('[E] Directory given in path does not exists!');
			self.__v('Checking target...');
			if not os.path.exists(self.__target):
				self.__v('Directory %s not found, trying to create...' % self.__target);
				os.mkdir(self.__target);
			self.__v('Checking access in target directory...');
			if not os.access(self.__target, os.W_OK):
				raise Exception('[E] Target directory is not writable!');
		except OSError:
			print('[E] Cannot create target directory');
			sys.exit(2);
		except Exception as err:
			print(err);
			sys.exit(2);

	def __v(self, text):
		if self.__verbose:
			print('[V] %s' % text);
	
	def __organize(self, path):
		try:
			files = os.listdir(path);
		except OSError:
			print('[W] Cannot list directory %s...' % path);
			return;
		covers = [];
		lastTag = None;
		for f in files:
			if os.path.islink(path + f) and not self.__follow:
				self.__v('Skipping link %s...' % path + f);
				continue;
			if os.path.isdir(path + f) and self.__recursive:
				self.__organize(path + f + '/');
			if f[-4:].lower() == '.mp3':
				lastTag = self.__getTag(path + f);
				self.__moveTrack(path + f, lastTag);
			if self.__recognizeCovers:
				if f[f.rfind('.'):].lower() in ('.jpg', '.gif', '.png', '.bmp', '.jpeg'):
					covers.append(path + f);
		if lastTag != None and len(covers) != 0:
			self.__moveCovers(lastTag, covers);
		if not self.__copy and lastTag != None and self.__delete and path != self.__path:
			try:
				os.rmdir(path);
			except:
				try:
					if self.__force:
						os.rmdirs(path);
					else:
						raise Exception();
				except:
					print('[W] Unable to remove directory %s' % path);

	
	def __moveCovers(self, tags, covers):
		outputDir = self.__target + os.path.dirname(self.__scheme.format(**tags));
		i = 1;
		for c in covers:
			self.__v('Found cover %s...' % c);
			ext = c[c.rfind('.'):];
			output = outputDir + '/cover' + ext;
			if c != output:
				while os.path.exists(output):
					output = outputDir + '/cover-' + str(i) + ext;
					i += 1;
				if self.__copy:
					self.__v('Copying cover %s -> %s' % (c, output));
					shutil.copy2(c, output);
				else:
					self.__v('Moving cover %s -> %s' % (c, output));
					shutil.move(c, output);	
			else:
				self.__v('Skipping %s' % c);

	def __getTag(self, track):
		oldName = os.path.basename(track);
		try:
			tag = stagger.read_tag(track);
			tags = {'artist':tag.artist or 'Unknown artist', 
			'album':tag.album or 'Unknown album', 
			'date':tag.date or 'XXXX', 
			'title':tag.title or 'Unknown title', 
			'genre':tag.genre or 'Unknown genre', 
			'track':tag.track or 'XX',
			'old-file-name':oldName[0:oldName.rfind('.')]};
		except stagger.errors.NoTagError as err:
			print('[W] Track %s has no ID3 tags...' % track);
			tags = {'artist':'Unknown artist', 
			'album':'Unknown album', 
			'date':'XXXX', 
			'title':'Unknown title', 
			'genre':'Unknown genre', 
			'track':'XX',
			'old-file-name':oldName[0:oldName.rfind('.')]};

		return tags;	

	def __moveTrack(self, track, tags):
		output = self.__target + self.__scheme.format(**tags) + track[-4:].lower();
		outputDir = os.path.dirname(output);
		if not os.path.exists(outputDir):
			self.__v('Creating output directories...');
			os.makedirs(outputDir);
		i = 1;
		ext = output[output.rfind('.'):];
		name = os.path.basename(output[0:output.rfind('.')]);
		if track != output:
			while os.path.exists(output):
				output = outputDir + '/' + name + '-' + str(i) + ext;
				i += 1;
			if self.__copy:
				self.__v('Copying %s -> %s' % (track, output));
				shutil.copy2(track, output);
			else:
				self.__v('Moving %s -> %s' % (track, output));
				shutil.move(track, output);
		else:
			self.__v('Skipping %s...' % track)

if __name__ == "__main__":
	organizer();
