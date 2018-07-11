const path = require('path');

const getContentType = (fileName = '') => {
    const fileExt = path.extname(fileName);
    switch (fileExt) {
    case '.js': {
        return 'application/javascript';
    }
    case '.css': {
        return 'text/css';
    }
    default: {
        return '';
    }
    }
};

const config = {
    options: {
        blobService: 'jabongassets',
        container: {
            options: {
                publicAccessLevel: 'blob'
            }
        },
        metadata: {
            contentType: getContentType,
            contentEncoding: 'gzip',
            cacheControl: 'public, max-age=31536000, s-maxage=31536000'
        },
        compression: {
            required: true,
            options: {
                level: 9
            }
        }
    }
};

module.exports = config;
