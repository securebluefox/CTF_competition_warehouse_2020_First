#include <sys/types.h>
#include <sys/stat.h>
#include <sys/ioctl.h>
#include <dirent.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdio.h>
#include <pwd.h>
#include <linux/fs.h>

#define BUFSIZE 256
#define MAX_ENTRIES 16

int protect(const char *flag_path)
{
	int fd;
	int attr;

	fd = open(flag_path, O_RDONLY);
	ioctl(fd, FS_IOC_GETFLAGS, &attr);
	attr |= FS_IMMUTABLE_FL;

	if (ioctl(fd, FS_IOC_SETFLAGS, &attr) < 0)
	{
		perror("IOCTL ERROR");
		printf("Please report to admin.\n");
		return 1;
	}

	close(fd);
	return 0;
}

int unprotect(const char *flag_path)
{
	int fd, attr;

	fd = open(flag_path, O_RDONLY);
	ioctl(fd, FS_IOC_GETFLAGS, &attr);
	attr ^= FS_IMMUTABLE_FL;

	if (ioctl(fd, FS_IOC_SETFLAGS, &attr) < 0)
	{
		perror("IOCTL ERROR");
		printf("Please report to admin.\n");
		return 1;
	}

	close(fd);
	return 0;
}

int copy(const char *src, const char *dst)
{
	char *content;
	FILE *file;
	int attr, flag_fd;

	file = fopen(src, "r");
	if (ferror(file))
		return 1;

	content = malloc(BUFSIZE);
	fread(content, BUFSIZE, 1, file);
	fclose(file);

	file = fopen(dst, "w");
	if (ferror(file))
	{
		free(content);
		return 1;
	}

	chmod(dst, S_IRUSR | S_IWUSR);
	fwrite(content, strlen(content) + 1, 1, file);
	fclose(file);

	free(content);
	return 0;
}

int setup(char **argv, char *dst_path)
{
	char *tmp_path = malloc(BUFSIZE);
	struct passwd *pwd;
	int attr;

	strncpy(tmp_path, argv[1], BUFSIZE);
	realpath(tmp_path, dst_path);
	strncpy(tmp_path, dst_path, BUFSIZE);

	if (!dst_path || strstr(dst_path, "/tmp/") != dst_path)
	{
		printf("Please work in a temporary folder under /tmp/\n");
		free(tmp_path);
		return 1;
	}

	strcat(tmp_path, "/flag");
	remove(tmp_path);
	copy("/home/catall/flag", tmp_path);

	free(tmp_path);
	return 0;
}

int main(int argc, char **argv)
{
	char *file_content;
	char *dir_path;
	char *file_path;
	char *flag_path;
	struct dirent **entries, *entry;
	FILE *file;
	int i, n, attr, flag_fd;

	if (argc != 2)
	{
		printf("Usage: catall.c /tmp/<your_folder>\n");
		return 1;
	}

	dir_path = malloc(BUFSIZE);
	if (setup(argv, dir_path))
	{
		free(dir_path);
		return 1;
	}

	flag_path = malloc(BUFSIZE);
	snprintf(flag_path, BUFSIZE, "%s/flag", dir_path);
	if (protect(flag_path))
	{
		remove(flag_path);
		free(flag_path);
		free(dir_path);
		return 1;
	}

	if ((n = scandir(dir_path, &entries, NULL, alphasort)) == -1)
	{
		printf("Directory Error\n");
		free(flag_path);
		free(dir_path);
		return 1;
	}

	file_content = malloc(BUFSIZE);
	file_path = malloc(BUFSIZE);

	for (i = 0; i < n && i < MAX_ENTRIES; i++)
	{
		entry = entries[i];
		snprintf(file_path, BUFSIZE, "%s/%s", dir_path, entry->d_name);

		if (entry->d_type == DT_REG)
		{
			printf("%s:\n", entry->d_name);
			file = fopen(file_path, "r");

			if (file != NULL)
			{
				memset(file_content, 0, BUFSIZE);
				fread(file_content, BUFSIZE, 1, file);
			}

			if (!strstr(file_path, "flag"))
			{
				printf("%s\n", file_content);
				memset(file_content, 0, BUFSIZE);
			}
		}
	}

	free(file_content);
	free(file_path);
	free(dir_path);

	if (!unprotect(flag_path))
		remove(flag_path);
	free(flag_path);

	return 0;
}
