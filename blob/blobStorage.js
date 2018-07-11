#!/usr/bin/env node

/**
 * This script is used to push the files with a specific content type
 * and gzip.
 */
/* eslint-disable no-console */

const zlib = require('zlib');
const azure = require('azure-storage');
const fs = require('fs');
const util = require('util');

const args = process.argv.slice(2);
const [folderPath, key, name = 'live'] = args;
let blob;

const { options: {
    blobService,
    container: { options },
    metadata,
    compression: {
        required,
        options: compressionOptions
    }
} } = require('./config');

const readdirAsync = util.promisify(fs.readdir);
const readFile = util.promisify(fs.readFile);
const gzip = util.promisify(zlib.gzip);

const getAssets = async (configPath, throwError) => {
    try {
        const files = await readdirAsync(configPath);
        return files;
    } catch (err) {
        if (throwError) throw err;
    }
    return [];
};

const getContentSettings = (meta = {}, filePath) => {
    const { contentType = '' } = meta;
    return {
        ...meta,
        contentType: typeof contentType === 'function' ? contentType(filePath)
            : contentType
    };
};

const compress = (input) => {
    if (!required) {
        return input;
    }
    return gzip(input, compressionOptions);
};

const traverseAndPush = async (folder) => {
    try {
        const assets = await getAssets(folder);
        console.log(assets, folder);
        assets.forEach(async (asset) => {
            const updatedPath = `${folder}/${asset}`;
            if (!fs.lstatSync(updatedPath).isDirectory()) {
                console.log(asset, 'is a file');
                const file = await readFile(updatedPath);
                const compressedFile = await compress(file);
                const filePath = updatedPath.replace('./assets/', '');
                blob.createBlockBlobFromText(
                    name,
                    filePath,
                    compressedFile,
                    { contentSettings: getContentSettings(metadata, filePath) },
                    (err) => {
                        if (!err) {
                            console.log(`successfully uploaded ${filePath} to container ${name}`);
                        } else {
                            console.error(err);
                        }
                    });
            } else {
                traverseAndPush(updatedPath);
            }
        });
    } catch (e) {
        console.log(e);
    }
};

const createConnection = () => {
    if (!folderPath) {
        return;
    }
    blob = azure.createBlobService(blobService, key);
    blob.createContainerIfNotExists(name, options, (error) => {
        if (!error) {
            console.log('Connection established', name, options);
            traverseAndPush(folderPath);
        }
        console.error(error);
    });
};

createConnection();
