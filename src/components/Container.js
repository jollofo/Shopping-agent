
export default function Container({children}){
    return (
        <>
            <div className="my-16 max-width-[1200px] place-items-center">{children}</div>
        </>
    )
}