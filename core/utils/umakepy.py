# -*- coding: utf-8 -*-
"""
@time           : 2019/5/24 下午10:22
@author         : liuning11@jd.com
@site           :
@file           : umake.py
@description    : make
"""
import argparse
import os
import platform
import zipfile
import sys
import logging

# 文件排除列表
__exclude = {
    "test*"
    ".pyc"
}


def is_miss_deploy_file(ddir, df):
    """
    部署文件是否存在
    :param ddir: string
    :param df: string
    :return:
    """
    path = os.path.join(ddir, "%s.py" % df)
    return __is_exist(path)


def __is_exist(f):
    """
    路径是否存在
    :param f:
    :return:
    """
    isExist = os.path.exists(f)
    print("%s is %s." % (f, 'existed' if isExist else 'not existed'))
    return isExist


def make_deploy_dir(project_dir, deploy_env):
    """
    创建部署目录
    :param project_dir: string 项目路径
    :param deploy_env: dict 部署环境变量
    :return:
    """

    name, path = loc_path(project_dir, deploy_env.deploy_dir)
    d_dir = os.path.join(path, name)
    d_name = os.path.join(d_dir, deploy_env.deploy_name)

    is_exist = os.path.exists(d_name)
    # if is_exist:
    #     shutil.rmtree(d_name)

    if not os.path.exists(d_dir):
        os.mkdir(d_dir)
    if not os.path.exists(d_name):
        os.mkdir(d_name)

    return d_name


def loc_path(current_dir, loc_path):
    """
    定位库位置
    :param cdir:
    :param lib_path:
    :return:
    """
    os.chdir(current_dir)
    paths = loc_path.split(os.sep)
    name = paths[-1]
    paths = paths[:-1]
    for p in paths:
        if p == '..':
            os.chdir(p)
        else:
            os.chdir(p)

    print('loc_path=====')
    print(os.getcwd())
    return name, os.getcwd()


def make_libs(cdir, deploy_path, deploy_env):
    """
    打包多个库
    :param cdir:
    :param deploy_path:
    :param deploy_env: dict 部署环境
    :return:
    """
    print('make libs...')
    for lib_path in deploy_env.lib:
        name, path = loc_path(cdir, lib_path)
        zdir = os.path.join(deploy_path, name)
        make_lib_src(name, path, zdir, deploy_env.exclude)


def make_lib_src(lib_name, lib_path, deploy_path, exclude):
    """
    源代码打包单个库
    :param lib_name: string 库名
    :param lib_path: string 库路径
    :param deploy_path: string 部署路径
    :return:
    """
    print('    <%s> to <%s>' % (os.path.join(lib_path, lib_name), deploy_path))

    os.chdir(lib_path)

    zf = zipfile.ZipFile(deploy_path + '.zip', "w")

    for parent, dirnames, filenames in os.walk(lib_name):
        for filename in filenames:
            if filename.lower().split('.')[0] not in exclude:
                pathfile = os.path.join(parent, filename)  # filename.encode('cp437').decode('utf8')
                print('      %s' % pathfile)
                zf.write(pathfile)

    zf.close()


def make_lib_c(lib_name, lib_path, deploy_path):
    """
    pyc打包单个库
    :param lib_name: string jszt_core_py
    :param lib_path: string 库路径
    :param deploy_path: string 部署文件路径
    :return:
    """
    lib_path = os.path.join(lib_path, lib_name)
    zip_path = "%s.zip" % deploy_path
    zf = zipfile.PyZipFile(zip_path, mode='w')

    try:
        zf.debug = 3
        zf.writepy(lib_path)
        return zip_path
    finally:
        zf.close()


def move_file(sourceDir, targetDir, deploy_env):
    """
    复制目录
    :param sourceDir:
    :param targetDir:
    :param deploy_env:
    :return:
    """

    def is_include(c, excludes):
        for e in excludes:
            if e in c:
                return True
        return False

    def is_eq(c, excludes):
        for e in excludes:
            if c == e:
                return True
        return False

    print('cp file...')
    # dd = deploy_env.deploy_dir
    # dd = str(dd[dd.rindex('/') + 1:])
    for f in os.listdir(sourceDir):
        sourceF = os.path.join(sourceDir, f)
        targetF = os.path.join(targetDir, f)
        if os.path.isfile(sourceF):
            if not is_include(f, deploy_env.exclude):  # f not in deploy_env.exclude
                if not os.path.exists(targetDir):
                    os.makedirs(targetDir)

                print('     <%s> to <%s>...' % (sourceF, targetF))
                open(targetF, "wb").write(open(sourceF, "rb").read())

        if os.path.isdir(sourceF):
            if not is_eq(f, deploy_env.exclude):  # f not in deploy_env.exclude
                move_file(sourceF, targetF, deploy_env)


def is_valid_deploy_env(deploy_env):
    """
    验证
    :param deploy_env:
    :return:
    """
    if not hasattr(deploy_env, 'deploy_dir'):
        raise Exception('has no deploy_dir attrib.')

    if not hasattr(deploy_env, 'deploy_name'):
        raise Exception('has no deploy_name attrib.')

    if not hasattr(deploy_env, 'lib'):
        raise Exception('has no libs attrib.')

    if not hasattr(deploy_env, 'exclude'):
        raise Exception('has no exclude attrib.')


def is_include(exclude, f):
    pass


def what_is_platform():
    if str(platform.system()).lower()[0:3] == 'win':
        return True
    else:
        return False


def identity_platform(deploy):
    if what_is_platform():
        deploy.deploy_dir = str(deploy.deploy_dir).replace('/', '\\')
        deploy.lib = [str(l).replace('/', '\\') for l in deploy.lib]
        deploy.exclude = deploy.exclude
    return deploy


def make(project_dir, deploy_file='__deploy__'):
    pd = project_dir
    pd = pd.replace('/', "\\") if what_is_platform() else pd
    df = deploy_file

    os.chdir(pd)
    pdir = os.getcwd()
    sys.path.append(pdir)

    isMissDf = is_miss_deploy_file(pdir, df)
    if not isMissDf:
        raise Exception("deploy file %s.py is not exist." % df)

    deploy = __import__(df)
    deploy = identity_platform(deploy)
    setattr(deploy, 'exclude', __exclude if not hasattr(deploy, 'exclude') else deploy.exclude | __exclude)

    is_valid_deploy_env(deploy)

    dir = make_deploy_dir(pdir, deploy)
    make_libs(pdir, dir, deploy)
    move_file(pdir, dir, deploy)

    print('')
    print(' %s deploy done.' % (deploy.deploy_name))


if __name__ == "__main__":
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument("-pd", "--pd", help="project dir项目目录，相对路径或绝对路径，必填", required=True)
    parser.add_argument("-df", "--df", help="deploy file部署文件", default='__deploy__', required=False)
    args = parser.parse_args()

    pd = args.pd
    pd = pd.replace('/', "\\") if what_is_platform() else pd
    df = args.df

    make(pd, df)
