document.addEventListener('DOMContentLoaded', () => {
    const scrollContainer: HTMLElement | null = document.querySelector('.image-scroll');
    const firstImageBlock: HTMLElement | null = document.querySelector('.block1');
    const leftArrow: HTMLElement | null = document.querySelector('.left-arrow');
    const rightArrow: HTMLElement | null = document.querySelector('.right-arrow');

    if (!scrollContainer || !firstImageBlock || !leftArrow || !rightArrow) {
        console.error('Не удалось найти необходимые элементы DOM');
        return;
    }

    const getImageBlockWidth = (): number => {
        return firstImageBlock.clientWidth + 10;
    };

    const scrollToCenter = (): void => {
        const imageBlockWidth: number = getImageBlockWidth();
        scrollContainer.scrollTo({
            left: imageBlockWidth * 4,
            behavior: 'smooth'
        });
    };

    const handleLeftArrowClick = (): void => {
        scrollContainer.scrollBy({
            left: -getImageBlockWidth(),
            behavior: 'smooth'
        });
    };

    const handleRightArrowClick = (): void => {
        scrollContainer.scrollBy({
            left: getImageBlockWidth(),
            behavior: 'smooth'
        });
    };

    setTimeout(scrollToCenter, 100);
    
    leftArrow.addEventListener('click', handleLeftArrowClick);
    rightArrow.addEventListener('click', handleRightArrowClick);
});